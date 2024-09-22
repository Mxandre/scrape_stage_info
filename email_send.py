import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

sender_email = "qiudongc"
sender_password = "13570346377Qiu!"

smtp_serveur = "smtps.utc.fr"
port = 465
serveur = smtplib.SMTP_SSL(smtp_serveur, port)
serveur.login(sender_email, sender_password)


# 要发送的邮箱和职位
data = pd.read_csv("stage_with_jobs.csv")
emails = data["courriel"].to_list()
jobs = data["job"].to_list()

for i in range(len(jobs)):

    # receiver_email =emails[i]
    receiver_email = emails[i]
    # test
    subject = f"Candidature pour le poste de stagiaire en {jobs[i]}"
    body = f"""Madame, Monsieur,

    Je vous adresse ma candidature pour le poste de stagiaire en {jobs[i]} au sein de votre entreprise. Actuellement étudiant(e) en Génie Informatique à l'Université de Technologie de Compiègne, et fort(e) d'une expérience  significative dans l'analyse de données et l'intelligence artificielle, je suis particulièrement enthousiaste à l'idée de mettre en pratique mes compétences et d'apprendre au sein de votre équipe.

    Vous trouverez en pièce jointe mon CV, qui détaille mes qualifications et mon parcours académique. Je serais ravi(e) de discuter plus en détail de ma candidature lors d'un entretien.

    Je vous remercie pour l'attention que vous porterez à ma demande et reste à votre disposition pour toute information complémentaire.Vous pouvez me joindre au 07 66 72 16 40 ou par email à dongcheng.qiu@etu.utc.fr.

    Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

    Cordinalement
    Dongcheng QIU"""
    msg = MIMEMultipart()
    msg["from"] = sender_email
    msg["to"] = receiver_email
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # 附件
    file_path = "profile.pdf"
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # 进行编码
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {file_name}")

    # 添加附件
    msg.attach(part)

    try:
        serveur.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"邮件已发送到{receiver_email}")
    except:
        print("this throws a bug")


serveur.quit()
