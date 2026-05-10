import boto3

def configurar_sns():
    sns = boto3.client('sns', region_name='us-east-1')
    
    # 1. Crear el Tema (Topic)
    topic = sns.create_topic(Name='AlertasMonitoreo')
    topic_arn = topic['TopicArn']
    
    # 2. Suscribir tu correo
    # REEMPLAZA 'tu-correo@ejemplo.com' con el tuyo real
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint='francisco.duenas7744@alumnos.udg.mx' 
    )
    
    print(f"Topic creado. ARN: {topic_arn}")
    print("REVISA TU CORREO y confirma la suscripción (dale clic al link que te llegó).")
    return topic_arn

if __name__ == "__main__":
    configurar_sns()