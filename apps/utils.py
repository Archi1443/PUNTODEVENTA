import smtplib
from email.mime.text import MIMEText
from email.header import Header

def enviar_correo(destinatario, asunto, mensaje):
    try:
        # Crear un objeto MIMEText que soporte UTF-8
        mensaje_mime = MIMEText(mensaje, 'plain', 'utf-8')
        mensaje_mime['From'] = 'avisos@techsolutionsobregon.com'
        mensaje_mime['To'] = destinatario
        mensaje_mime['Subject'] = Header(asunto, 'utf-8')

        # Configuración del servidor SMTP
        server = smtplib.SMTP('smtp.hostinger.com', 587)
        server.starttls()
        server.login('avisos@techsolutionsobregon.com', 'YahirPendejo@7')
        
        # Enviar el correo
        server.sendmail('avisos@techsolutionsobregon.com', [destinatario], mensaje_mime.as_string())
        server.quit()
        print("Correo enviado exitosamente a", destinatario)
    except Exception as e:
        print("Error al enviar correo a", destinatario, ":", e)
