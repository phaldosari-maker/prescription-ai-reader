import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- إعدادات الصفحة ---
st.set_page_config(page_title="محلل الوصفات (Gemini 1.5)", layout="centered")
st.title("🩺 الدوسري قارئ الوصفات الطبية")

# --- إدخال المفتاح ---
api_key = st.text_input("أدخل مفتاح Google API Key:", type="password")

# --- دالة التحليل ---
def analyze_prescription_gemini(api_key, image):
    try:
        genai.configure(api_key=api_key)
        
        # --- (تغيير مهم) نستخدم الاسم الأحدث للموديل ---
        model_name = 'gemini-1.5-flash-latest' 
        
        # إنشاء الموديل
        model = genai.GenerativeModel(model_name)
        
        prompt = """
        أنت صيدلي خبير. استخرج أسماء الأدوية والجرعات من هذه الوصفة الطبية.
        اكتب النتيجة في جدول واضح باللغة العربية.
        """
        
        response = model.generate_content([prompt, image])
        return response.text

    except Exception as e:
        # هذا السطر سيطبع الخطأ بالتفصيل
        return f"خطأ: {e}"

# --- واجهة الرفع ---
uploaded_file = st.file_uploader("ارفع صورة الوصفة", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الوصفة المرفقة', use_column_width=True)
    
    if st.button("🔍 تحليل الوصفة"):
        if not api_key:
            st.error("الرجاء إدخال المفتاح")
        else:
            with st.spinner('جاري الاتصال...'):
                result = analyze_prescription_gemini(api_key, image)
                
                # إذا كان هناك خطأ يحتوي على كلمة 404، نعطي نصيحة
                if "404" in result:
                    st.error(result)
                    st.warning("⚠️ لا يزال هناك مشكلة في الاتصال. تأكد من أن الـ VPN يعمل على وضع (All Traffic) وليس فقط المتصفح.")
                else:
                    st.success("تم!")
                    st.markdown(result)
