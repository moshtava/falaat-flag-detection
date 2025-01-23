import MetaTrader5 as mt5
import pandas as pd
import logging
from decouple import config

logger = logging.getLogger(__name__)


def connect_mt5():
    """
    Initializes and establishes a connection to MetaTrader 5.
    
    Returns:
        bool: True if connection is successful.
    
    Raises:
        ConnectionError: If initialization fails.
    """
    account = config('MT5_ACCOUNT', cast=int)  
    password = config('MT5_PASSWORD')  
    server = config('MT5_SERVER')  

    if not mt5.initialize(login=account, password=password, server=server):
        error_code, description = mt5.last_error()
        error_message = (
            f"MetaTrader 5 initialization failed. Error Code: {error_code}, Description: {description}"
        )
        logger.error(error_message)
        raise ConnectionError(error_message)

    logger.info("MetaTrader 5 initialized and logged in successfully.")
    return True


def get_eurusd_data(symbol='EURUSD', timeframe=mt5.TIMEFRAME_M1, bars=500):
    """
    Fetches historical price data for the specified financial instrument.
    
    Parameters:
        symbol (str): Symbol for the financial instrument (default: 'EURUSD').
        timeframe (int): Timeframe constant (default: `mt5.TIMEFRAME_M1`).
        bars (int): Number of bars to fetch (default: 500).
    
    Returns:
        pd.DataFrame: DataFrame containing the historical data.
    
    Raises:
        ValueError: If data retrieval fails or the data is empty.
    """
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    
    if rates is None or len(rates) == 0:
        error_code, description = mt5.last_error()
        error_message = (
            f"Failed to retrieve data for {symbol}. "
            f"Error Code: {error_code}, Description: {description}"
        )
        logger.error(error_message)
        raise ValueError(error_message)

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')  # Convert Unix time to datetime

    logger.info(f"Successfully retrieved {len(data)} bars for {symbol}.")
    return data


def validate_data(data, required_columns, min_rows=50):
    """
    Validates the input DataFrame for required columns and minimum rows.
    
    Parameters:
        data (pd.DataFrame): Input data.
        required_columns (set): Required column names.
        min_rows (int): Minimum number of rows required.
    
    Returns:
        bool: True if validation passes, raises an error otherwise.
    """
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Input data must contain the following columns: {required_columns}")
    if len(data) < min_rows:
        raise ValueError(f"Input data must contain at least {min_rows} rows.")
    return True


def detect_flagpole(data, start_idx, end_idx, threshold=0.02):
    """
    Detects the flagpole in the data.

    Parameters:
        data (pd.DataFrame): Input data with a 'close' column.
        start_idx (int): Start index of the flagpole window.
        end_idx (int): End index of the flagpole window.
        threshold (float): Percentage change threshold for a sharp move.

    Returns:
        bool: True if a flagpole is detected, False otherwise.
    """
    if start_idx < 0 or end_idx > len(data) or start_idx >= end_idx:
        raise ValueError(f"Invalid indices: start_idx={start_idx}, end_idx={end_idx}")
    flagpole_window = data['close'].iloc[start_idx:end_idx]
    percentage_change = (flagpole_window.iloc[-1] - flagpole_window.iloc[0]) / flagpole_window.iloc[0]

    return percentage_change > threshold


def detect_consolidation(data, start_idx, end_idx, threshold=0.01):
    """
    Detects consolidation in the data.
    
    Parameters:
        data (pd.DataFrame): Input data with a 'close' column.
        start_idx (int): Start index of the consolidation window.
        end_idx (int): End index of the consolidation window.
        threshold (float): Maximum allowed range relative to average price.
    
    Returns:
        bool: True if consolidation is detected, False otherwise.
    """
    consolidation_window = data['close'].iloc[start_idx:end_idx]
    consolidation_range = consolidation_window.max() - consolidation_window.min()
    average_price = consolidation_window.mean()
    return consolidation_range <= (average_price * threshold)


def detect_breakout(data, start_idx, threshold=0.03):
    """
    Detects a breakout in the data.
    
    Parameters:
        data (pd.DataFrame): Input data with a 'close' column.
        start_idx (int): Start index of the breakout window.
        threshold (float): Minimum total percentage change for a breakout.
    
    Returns:
        bool: True if a breakout is detected, False otherwise.
    """
    breakout_window = data['close'].iloc[start_idx:]
    cumulative_change = (breakout_window.iloc[-1] - breakout_window.iloc[0]) / breakout_window.iloc[0]
    return cumulative_change > threshold


def detect_flag_pattern(data):
    """
    Detects a professional-grade flag pattern in financial data.

    Parameters:
        data (pd.DataFrame): DataFrame containing at least the 'close' price column.
    
    Returns:
        dict: If a flag pattern is detected, returns time and price details. Otherwise, None.
    """
    required_columns = {'time', 'close'}
    validate_data(data, required_columns)
    
    flagpole_start, flagpole_end = -30, -20
    consolidation_start, consolidation_end = -20, -5
    breakout_start = -5
    
    is_flagpole = detect_flagpole(data, flagpole_start, flagpole_end)
    is_consolidation = detect_consolidation(data, consolidation_start, consolidation_end)
    is_breakout = detect_breakout(data, breakout_start)
    
    if is_flagpole and is_consolidation and is_breakout:
        return {
            "time": data.iloc[-1]['time'],
            "price": data.iloc[-1]['close'],
            "details": {
                "flagpole_start_time": data.iloc[flagpole_start]['time'],
                "flagpole_end_time": data.iloc[flagpole_end]['time'],
                "consolidation_start_time": data.iloc[consolidation_start]['time'],
                "consolidation_end_time": data.iloc[consolidation_end]['time'],
                "breakout_start_time": data.iloc[breakout_start]['time'],
            }
        }
    
    return None