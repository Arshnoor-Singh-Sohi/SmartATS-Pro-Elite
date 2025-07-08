import streamlit as st
from typing import Any, Optional

class SessionManager:
    """
    Manages Streamlit session state for persistent data across interactions
    """
    
    def __init__(self):
        # Initialize default session values if they don't exist
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """Initialize default session state values"""
        defaults = {
            'uploaded_file': None,
            'file_name': None,
            'resume_text': '',
            'job_description': '',
            'analysis_result': None,
            'analysis_timestamp': None,
            'is_edited': False,
            'rescore_count': 0,
            'keyword_suggestions': [],
            'session_id': None,
            'user_preferences': {
                'theme': 'light',
                'auto_save': True,
                'show_tips': True
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from session state
        
        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value from session state or default
        """
        return st.session_state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in session state
        
        Args:
            key: The key to set
            value: The value to store
        """
        st.session_state[key] = value
    
    def update(self, updates: dict) -> None:
        """
        Update multiple values in session state
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        for key, value in updates.items():
            st.session_state[key] = value
    
    def clear(self, keys: Optional[list] = None) -> None:
        """
        Clear session state
        
        Args:
            keys: Optional list of specific keys to clear. If None, clears all.
        """
        if keys:
            for key in keys:
                if key in st.session_state:
                    del st.session_state[key]
        else:
            # Clear all except user preferences
            preserved_keys = ['user_preferences']
            keys_to_clear = [k for k in st.session_state.keys() if k not in preserved_keys]
            for key in keys_to_clear:
                del st.session_state[key]
            
            # Re-initialize defaults
            self._initialize_defaults()
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in session state
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        return key in st.session_state
    
    def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment a numeric value in session state
        
        Args:
            key: The key to increment
            amount: Amount to increment by
            
        Returns:
            The new value
        """
        current = self.get(key, 0)
        new_value = current + amount
        self.set(key, new_value)
        return new_value
    
    def append(self, key: str, value: Any) -> list:
        """
        Append to a list in session state
        
        Args:
            key: The key of the list
            value: Value to append
            
        Returns:
            The updated list
        """
        current_list = self.get(key, [])
        if not isinstance(current_list, list):
            current_list = []
        current_list.append(value)
        self.set(key, current_list)
        return current_list
    
    def get_analysis_history(self) -> list:
        """
        Get the history of analyses performed in this session
        
        Returns:
            List of analysis records
        """
        return self.get('analysis_history', [])
    
    def add_to_history(self, analysis_record: dict) -> None:
        """
        Add an analysis record to history
        
        Args:
            analysis_record: Dictionary containing analysis details
        """
        history = self.get_analysis_history()
        history.append(analysis_record)
        self.set('analysis_history', history)
        
        # Keep only last 10 analyses
        if len(history) > 10:
            self.set('analysis_history', history[-10:])
    
    def get_session_stats(self) -> dict:
        """
        Get statistics about the current session
        
        Returns:
            Dictionary containing session statistics
        """
        return {
            'rescore_count': self.get('rescore_count', 0),
            'analyses_performed': len(self.get_analysis_history()),
            'has_resume': bool(self.get('resume_text')),
            'has_job_description': bool(self.get('job_description')),
            'is_edited': self.get('is_edited', False),
            'session_duration': None  # Could implement with timestamp tracking
        }
    
    def export_session_data(self) -> dict:
        """
        Export all session data (useful for debugging or saving)
        
        Returns:
            Dictionary containing all session data
        """
        return {
            key: value for key, value in st.session_state.items()
            if not key.startswith('_')  # Skip internal Streamlit keys
        }
    
    def import_session_data(self, data: dict) -> None:
        """
        Import session data from a dictionary
        
        Args:
            data: Dictionary containing session data to import
        """
        for key, value in data.items():
            if not key.startswith('_'):  # Skip internal keys
                st.session_state[key] = value