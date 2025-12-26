"""Cấu hình OpenAI API"""
import os
from openai import OpenAI

# Khởi tạo OpenAI client
def get_openai_client():
    """Lấy OpenAI client với API key từ environment variable"""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        print(f"Lỗi khởi tạo OpenAI client: {e}")
        return None

def is_openai_available():
    """Kiểm tra xem OpenAI API có sẵn không"""
    return get_openai_client() is not None