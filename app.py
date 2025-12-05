import streamlit as st
import google.generativeai as genai

st.title("🛠 فحص موديلات جوجل")

api_key = st.text_input("ضع مفتاح API هنا للفحص:", type="password")

if st.button("افحص الموديلات المتاحة لي"):
    if not api_key:
        st.error("أدخل المفتاح أولاً")
    else:
        try:
            genai.configure(api_key=api_key)
            st.info("جاري الاتصال بجوجل لجلب القائمة...")
            
            # نطلب من جوجل قائمة الموديلات
            found_any = False
            for m in genai.list_models():
                # نبحث عن الموديلات التي تدعم إنشاء المحتوى (generateContent)
                if 'generateContent' in m.supported_generation_methods:
                    st.success(f"✅ موديل متاح: {m.name}")
                    found_any = True
            
            if not found_any:
                st.warning("⚠️ اتصلنا بجوجل ولكن القائمة فارغة! هذا يعني أن الحساب محظور جغرافياً.")
                
        except Exception as e:
            st.error(f"❌ خطأ في الاتصال: {e}")
            st.write("نصيحة: تأكد أن الـ VPN يعمل على اللابتوب بالكامل")
