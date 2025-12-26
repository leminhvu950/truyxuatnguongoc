"""AI nâng cao với OpenAI để phân tích sản phẩm và gợi ý tiêu chuẩn số hóa"""
import json
from datetime import datetime
from openai_config import get_openai_client, is_openai_available
import ai_analysis

def analyze_product_with_openai(product):
    """Phân tích sản phẩm với OpenAI để có gợi ý chi tiết hơn"""
    
    # Lấy phân tích cơ bản trước
    basic_analysis = ai_analysis.analyze_product_ai(product)
    
    # Nếu không có OpenAI, trả về phân tích cơ bản
    if not is_openai_available():
        basic_analysis['ai_enhanced'] = False
        basic_analysis['openai_suggestions'] = []
        return basic_analysis
    
    try:
        client = get_openai_client()
        
        # Chuẩn bị dữ liệu sản phẩm để gửi cho OpenAI
        product_data = {
            'name': product.get('product_name', ''),
            'type': product.get('product_type', ''),
            'farmer': product.get('farmer_name', ''),
            'area': product.get('production_area', ''),
            'planting_date': product.get('planting_date', ''),
            'harvest_date': product.get('harvest_date', ''),
            'production_process': product.get('production_process', ''),
            'harvest_process': product.get('harvest_process', ''),
            'storage_method': product.get('storage_method', ''),
            'has_production_media': len(product.get('production_media', [])) > 0,
            'has_harvest_media': len(product.get('harvest_media', [])) > 0,
            'transparency_score': basic_analysis['score']
        }
        
        # Tạo prompt cho OpenAI
        prompt = f"""
Bạn là chuyên gia nông nghiệp và số hóa nông sản tại Việt Nam. Hãy phân tích sản phẩm nông sản sau và đưa ra gợi ý cụ thể:

THÔNG TIN SẢN PHẨM:
- Tên sản phẩm: {product_data['name']}
- Loại sản phẩm: {product_data['type']}
- Nông dân: {product_data['farmer']}
- Khu vực sản xuất: {product_data['area']}
- Ngày trồng: {product_data['planting_date']}
- Ngày thu hoạch: {product_data['harvest_date']}
- Quy trình sản xuất: {product_data['production_process'][:200]}...
- Quy trình thu hoạch: {product_data['harvest_process'][:200]}...
- Phương pháp bảo quản: {product_data['storage_method'][:200]}...
- Có media sản xuất: {product_data['has_production_media']}
- Có media thu hoạch: {product_data['has_harvest_media']}
- Điểm minh bạch hiện tại: {product_data['transparency_score']}/100

HÃY PHÂN TÍCH VÀ ĐƯA RA:

1. ĐÁNH GIÁ CHẤT LƯỢNG THÔNG TIN:
- Điểm mạnh của thông tin hiện tại
- Điểm cần cải thiện
- Mức độ tuân thủ tiêu chuẩn số hóa nông sản

2. GỢI Ý CẢI THIỆN TIÊU CHUẨN SỐ HÓA:
- Thông tin cần bổ sung
- Cách cải thiện quy trình ghi chép
- Tiêu chuẩn chứng nhận nên áp dụng

3. PHÂN TÍCH THỊ TRƯỜNG:
- Tiềm năng thị trường cho sản phẩm này
- Giá cả dự kiến
- Kênh phân phối phù hợp
- Đối tượng khách hàng mục tiêu

4. GỢI Ý MARKETING:
- Cách quảng bá sản phẩm
- Điểm nhấn để thu hút khách hàng
- Chiến lược xây dựng thương hiệu

5. TUÂN THỦ QUY ĐỊNH:
- Các quy định pháp lý cần tuân thủ
- Giấy tờ, chứng nhận cần có
- Tiêu chuẩn an toàn thực phẩm

Trả lời bằng tiếng Việt, cụ thể và thực tế cho thị trường Việt Nam.
"""

        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia nông nghiệp và số hóa nông sản tại Việt Nam với kinh nghiệm 15 năm."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        ai_suggestions = response.choices[0].message.content
        
        # Thêm gợi ý OpenAI vào kết quả
        basic_analysis['ai_enhanced'] = True
        basic_analysis['openai_suggestions'] = ai_suggestions
        basic_analysis['openai_timestamp'] = datetime.now().isoformat()
        
        return basic_analysis
        
    except Exception as e:
        print(f"Lỗi khi gọi OpenAI API: {e}")
        basic_analysis['ai_enhanced'] = False
        basic_analysis['openai_error'] = str(e)
        return basic_analysis

def get_digitization_standards_suggestions(product):
    """Lấy gợi ý tiêu chuẩn số hóa cụ thể từ OpenAI"""
    
    if not is_openai_available():
        return {
            'available': False,
            'suggestions': []
        }
    
    try:
        client = get_openai_client()
        
        prompt = f"""
Bạn là chuyên gia về tiêu chuẩn số hóa nông sản. Hãy đưa ra danh sách cụ thể các tiêu chuẩn số hóa mà sản phẩm "{product.get('product_name', '')}" cần tuân thủ:

THÔNG TIN SẢN PHẨM:
- Tên: {product.get('product_name', '')}
- Loại: {product.get('product_type', '')}
- Khu vực: {product.get('production_area', '')}

HÃY ĐƯA RA DANH SÁCH CỤ THỂ:

1. TIÊU CHUẨN BẮT BUỘC:
- Các thông tin tối thiểu phải có
- Định dạng dữ liệu chuẩn
- Quy trình ghi chép bắt buộc

2. TIÊU CHUẨN NÂNG CAO:
- Chứng nhận chất lượng
- Tiêu chuẩn quốc tế có thể áp dụng
- Công nghệ số hóa nên sử dụng

3. CHECKLIST ĐÁNH GIÁ:
- Danh sách kiểm tra từng bước
- Tiêu chí đánh giá điểm số
- Mức độ tuân thủ

Trả lời dưới dạng JSON với cấu trúc:
{{
    "mandatory_standards": [
        {{"name": "Tên tiêu chuẩn", "description": "Mô tả", "status": "missing/partial/complete"}}
    ],
    "advanced_standards": [
        {{"name": "Tên tiêu chuẩn", "description": "Mô tả", "benefit": "Lợi ích"}}
    ],
    "checklist": [
        {{"item": "Mục kiểm tra", "required": true/false, "score": 0-10}}
    ]
}}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia tiêu chuẩn số hóa nông sản. Trả lời bằng JSON hợp lệ."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        try:
            suggestions_json = json.loads(response.choices[0].message.content)
            return {
                'available': True,
                'suggestions': suggestions_json,
                'timestamp': datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            return {
                'available': True,
                'suggestions': {
                    'raw_response': response.choices[0].message.content
                },
                'timestamp': datetime.now().isoformat()
            }
            
    except Exception as e:
        print(f"Lỗi khi lấy gợi ý tiêu chuẩn: {e}")
        return {
            'available': False,
            'error': str(e)
        }

def get_market_analysis(product):
    """Phân tích thị trường chi tiết với OpenAI"""
    
    if not is_openai_available():
        return {
            'available': False,
            'analysis': {}
        }
    
    try:
        client = get_openai_client()
        
        prompt = f"""
Phân tích thị trường cho sản phẩm nông sản sau tại Việt Nam:

SẢN PHẨM: {product.get('product_name', '')}
KHU VỰC: {product.get('production_area', '')}
THỜI GIAN THU HOẠCH: {product.get('harvest_date', '')}

HÃY PHÂN TÍCH:

1. GIÁ CẢ THỊ TRƯỜNG:
- Giá hiện tại (VNĐ/kg)
- Xu hướng giá 6 tháng tới
- Yếu tố ảnh hưởng giá

2. CUNG CẦU:
- Tình hình cung
- Nhu cầu thị trường
- Mùa vụ ảnh hưởng

3. KÊNH PHÂN PHỐI:
- Kênh bán lẻ
- Kênh bán buôn
- Kênh online
- Xuất khẩu

4. ĐỐI THỦ CẠNH TRANH:
- Sản phẩm cùng loại
- Lợi thế cạnh tranh
- Điểm khác biệt

5. CƠ HỘI KINH DOANH:
- Thị trường ngách
- Sản phẩm giá trị gia tăng
- Hợp tác liên kết

Trả lời bằng tiếng Việt, số liệu cụ thể cho thị trường Việt Nam.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia phân tích thị trường nông sản Việt Nam."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        
        return {
            'available': True,
            'analysis': response.choices[0].message.content,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Lỗi khi phân tích thị trường: {e}")
        return {
            'available': False,
            'error': str(e)
        }

def generate_improvement_plan(product, analysis):
    """Tạo kế hoạch cải thiện cụ thể với OpenAI"""
    
    if not is_openai_available():
        return {
            'available': False,
            'plan': {}
        }
    
    try:
        client = get_openai_client()
        
        prompt = f"""
Dựa trên phân tích sản phẩm, hãy tạo kế hoạch cải thiện cụ thể:

SẢN PHẨM: {product.get('product_name', '')}
ĐIỂM MINH BẠCH HIỆN TẠI: {analysis.get('score', 0)}/100
ĐIỂM TUÂN THỦ: {analysis.get('standards_compliance', {}).get('compliance_score', 0)}/100

VẤN ĐỀ CẦN KHẮC PHỤC:
{chr(10).join(analysis.get('recommendations', []))}

HÃY TẠO KẾ HOẠCH CẢI THIỆN:

1. MỤC TIÊU NGẮN HẠN (1-3 tháng):
- Hành động cụ thể
- Thời gian thực hiện
- Chi phí ước tính
- Kết quả mong đợi

2. MỤC TIÊU TRUNG HẠN (3-6 tháng):
- Nâng cấp quy trình
- Đầu tư công nghệ
- Đào tạo kỹ năng

3. MỤC TIÊU DÀI HẠN (6-12 tháng):
- Chứng nhận chất lượng
- Mở rộng thị trường
- Xây dựng thương hiệu

4. LỘTRÌNH THỰC HIỆN:
- Tuần 1-4: Làm gì
- Tháng 2-3: Làm gì
- Tháng 4-6: Làm gì

5. CHỈ SỐ ĐÁNH GIÁ:
- KPI cần theo dõi
- Cách đo lường tiến độ
- Mốc thời gian kiểm tra

Trả lời cụ thể, thực tế và có thể thực hiện được.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia tư vấn cải thiện quy trình nông nghiệp."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.6
        )
        
        return {
            'available': True,
            'plan': response.choices[0].message.content,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Lỗi khi tạo kế hoạch cải thiện: {e}")
        return {
            'available': False,
            'error': str(e)
        }