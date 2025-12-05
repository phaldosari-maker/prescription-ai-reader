import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- إعدادات الصفحة ---
st.set_page_config(page_title="محلل الوصفات (Gemini المجاااااني)", layout="centered")

# --- العنوان ---
st.title("🩺 قارئ الوصفات الطبية (مجاني)")
st.caption("يعمل بواسطة Google Gemini 1.5 Flash")

# --- إدخال المفتاح ---
# يمكنك وضع المفتاح هنا مباشرة إذا كان الاستخدام شخصي، لكن الأفضل إدخاله في الواجهة
api_key = st.text_input("أدخل مفتاح Google API Key المجاني:", type="password")
st.markdown("[احصل على مفتاح مجاني من هنا](https://aistudio.google.com/app/apikey)")

# --- دالة التحليل ---
def analyze_prescription_gemini(api_key, image):
    # إعداد جوجل
    genai.configure(api_key=api_key)
    
    # نستخدم موديل فلاش لأنه سريع ومجاني وكفؤ
    model = model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = """
    أنت صيدلي خبير ومساعد طبي بالذكاء الاصطناعي.
    قم بتحليل صورة الوصفة الطبية المرفقة بدقة عالية.
    
    المطلوب منك:
    1. استخراج أسماء الأدوية المكتوبة (حتى لو كان الخط سيئاً، حاول التوقع بناء على الأحرف الظاهرة).
    2. استخراج الجرعات وطريقة الاستخدام.
    3. ترجمة طريقة الاستخدام إلى اللغة العربية لتكون سهلة للمريض.
    
    نسق الإجابة بشكل جميل وواضح (جدول أو نقاط).
    """
    
    try:
        # إرسال الصورة والطلب
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"حدث خطأ: {e}"

# --- واجهة الرفع ---
uploaded_file = st.file_uploader("ارفع صورة الوصفة", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # عرض الصورة
    image = Image.open(uploaded_file)
    st.image(image, caption='الوصفة المرفقة', use_column_width=True)
    
    if st.button("🔍 تحليل الوصفة مجاناً"):
        if not api_key:
            st.error("الرجاء إدخال مفتاح Google API.")
        else:
            with st.spinner('جاري سؤال Google Gemini...'):
                result = analyze_prescription_gemini(api_key, image)
                st.success("تم التحليل!")
                st.markdown("### 📋 النتيجة:")
                st.markdown(result)
                st.warning("⚠️ تنبيه: الذكاء الاصطناعي قد يخطئ. راجع الصيدلي عبدالرحمن دائماً.")
