from typing import Optional

def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """
    Callback que se ejecuta de forma nativa antes de iniciar el flujo.
    Vincula el idLlamada (telefónico) con el session_id (conversación)
    directamente en Cloud Logging al inicio de la llamada con latencia cero.
    """
    # 1. Asegurar almacenamiento del session_id en el estado
    session_id = callback_context.session_id
    if callback_context.state.get("session_id", "") == "":
        callback_context.state["session_id"] = session_id

    # 2. Obtener el idLlamada (callid) enviado por la telefonía
    callid_raw = callback_context.variables.get("callid")
    
    # Formatear callid como entero sin decimales si viene como float
    id_llamada = "N/A"
    if callid_raw is not None:
        try:
            id_llamada = str(int(float(callid_raw)))
        except ValueError:
            id_llamada = str(callid_raw)

    # 3. Imprimir el log de vinculación inicial. 
    # Google Cloud Logging lo captura y lo indexa de inmediato de forma nativa.
    print(f"[Success] Vinculación inicial para idLlamada: {id_llamada} y session_id: {session_id}")
    
    return None