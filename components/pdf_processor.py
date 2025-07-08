import PyPDF2
import io
import streamlit as st
from typing import Optional
import re

class PDFProcessor:
    """
    Handles PDF processing and text extraction with multiple fallback methods
    """
    
    def __init__(self):
        self.extraction_methods = [
            self._extract_with_getvalue,
            self._extract_with_read,
            self._extract_with_pypdf2_direct
        ]
    
    def extract_text(self, uploaded_file) -> Optional[str]:
        """
        Extract text from PDF using multiple methods with fallbacks
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Extracted text content or None if extraction fails
        """
        if not uploaded_file:
            return None
        
        # Try each extraction method
        for method in self.extraction_methods:
            try:
                text = method(uploaded_file)
                if text and len(text.strip()) > 0:
                    # Clean and normalize the text
                    cleaned_text = self._clean_text(text)
                    return cleaned_text
            except Exception as e:
                continue
        
        # If all methods fail
        st.error("Failed to extract text from PDF. Please ensure the PDF contains readable text.")
        return None
    
    def _extract_with_getvalue(self, uploaded_file) -> str:
        """Extract using getvalue() method"""
        file_bytes = uploaded_file.getvalue()
        return self._process_bytes(file_bytes)
    
    def _extract_with_read(self, uploaded_file) -> str:
        """Extract using read() method with seek reset"""
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        return self._process_bytes(file_bytes)
    
    def _extract_with_pypdf2_direct(self, uploaded_file) -> str:
        """Extract using PyPDF2 directly on the file object"""
        uploaded_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return self._extract_from_reader(pdf_reader)
    
    def _process_bytes(self, file_bytes: bytes) -> str:
        """Process PDF bytes and extract text"""
        if not file_bytes:
            raise ValueError("Empty file bytes")
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return self._extract_from_reader(pdf_reader)
    
    def _extract_from_reader(self, pdf_reader) -> str:
        """Extract text from PyPDF2 reader object"""
        if pdf_reader.is_encrypted:
            raise ValueError("PDF is encrypted")
        
        text_content = ""
        num_pages = len(pdf_reader.pages)
        
        for page_num in range(num_pages):
            try:
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            except Exception:
                continue
        
        return text_content
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned and normalized text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common extraction issues
        text = text.replace('•', '-')  # Normalize bullet points
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        
        # Normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def get_pdf_metadata(self, uploaded_file) -> dict:
        """
        Extract metadata from PDF file
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Dictionary containing PDF metadata
        """
        try:
            uploaded_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            metadata = {
                'pages': len(pdf_reader.pages),
                'encrypted': pdf_reader.is_encrypted,
                'title': None,
                'author': None,
                'subject': None,
                'creator': None
            }
            
            if pdf_reader.metadata:
                metadata.update({
                    'title': pdf_reader.metadata.get('/Title'),
                    'author': pdf_reader.metadata.get('/Author'),
                    'subject': pdf_reader.metadata.get('/Subject'),
                    'creator': pdf_reader.metadata.get('/Creator')
                })
            
            return metadata
            
        except Exception as e:
            return {'error': str(e)}
    
    def validate_pdf(self, uploaded_file) -> tuple[bool, str]:
        """
        Validate PDF file
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not uploaded_file:
            return False, "No file uploaded"
        
        # Check file size (max 10MB)
        file_size = len(uploaded_file.getvalue())
        if file_size > 10 * 1024 * 1024:
            return False, "File size exceeds 10MB limit"
        
        # Check if it's actually a PDF
        try:
            uploaded_file.seek(0)
            header = uploaded_file.read(5)
            uploaded_file.seek(0)
            
            if header != b'%PDF-':
                return False, "File is not a valid PDF"
            
            # Try to open with PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            if pdf_reader.is_encrypted:
                return False, "PDF is password protected"
            
            if len(pdf_reader.pages) == 0:
                return False, "PDF has no pages"
            
            return True, "PDF is valid"
            
        except Exception as e:
            return False, f"PDF validation error: {str(e)}"