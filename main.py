import smtplib
from email.message import EmailMessage
import ssl
import streamlit as st


def send_email(from_email, password, to_email, subject, body, attachment_file):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    file_data = attachment_file.read()
    file_name = attachment_file.name
    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.yandex.com', 465, context=context) as server:
        server.login(from_email, password)
        server.send_message(msg)


def main():
    st.title("Отправка ПЦР-результатов")

    from_email = st.text_input("Введите ваш email (Яндекс)")
    password = st.text_input("Введите ваш пароль", type="password")
    pdf_files = st.file_uploader("Выберите PDF файлы", type=["pdf"], accept_multiple_files=True)
    email_input = st.text_area("Введите email адреса (через ;)", "")

    if st.button("Отправить"):
        if from_email and password and pdf_files and email_input:
            emails = email_input.split(';')
            emails = [email.strip() for email in emails]

            if len(emails) != len(pdf_files):
                st.error("Количество email-адресов и количество файлов должны совпадать.")
                return

            for email, pdf_file in zip(emails, pdf_files):
                try:
                    body = (
                        "Доброго времени суток!\n"
                        "\n"
                        "Это Центральный институт Эпидемиологии.\n"
                        "\n"
                        "Ранее Вы сдавали анализы на инфекции, передаваемые половым путем.\n"
                        "\n"
                        "Ваш результат ПЦР-теста во вложении."
                        "\n"
                        "Мы благодарим Вас за участие в исследовании!"
                    )
                    send_email(from_email, password, email, "Ваш результат ПЦР-теста", body, pdf_file)
                    st.success(f"Email отправлен на {email}")
                except Exception as e:
                    st.error(f"Не удалось отправить email на {email}.\nОшибка: {str(e)}")
        else:
            st.warning("Пожалуйста, введите email, пароль, загрузите PDF файлы и введите адреса.")


if __name__ == "__main__":
    main()