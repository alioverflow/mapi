import smtplib, ssl
import requests

def sendEmail():
            port = 465
            smtp_server_domain_name = "smtp.gmail.com"
            sender_mail = "jerry.zhang9139@gmail.com"
            password = "uuuaibpzkqpzfjge"
            ssl_context = ssl.create_default_context()
            service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
            service.login(sender_mail, password)
            url = 'https://api.themoviedb.org/3/movie/popular?api_key=6ad473f9a4be91546b3049c7a2654697&language=en-US&page=1'
            r = requests.get(url)
            data = r.json()
            films = data["results"][0]
            mails = "kaya87826@gmail.com"
            subject = films["title"]
            content = films["overview"]
            result = service.sendmail(sender_mail,mails,f"Subject : {subject}\n{content}")
            service.quit()
