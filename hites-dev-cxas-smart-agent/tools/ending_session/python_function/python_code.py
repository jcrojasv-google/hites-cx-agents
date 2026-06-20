def ending_session() -> dict:
  """
  Establece la bandera de finalización de sesión en el estado de la llamada.
  Retorna un diccionario estructurado indicando el éxito o instruyendo al agente en caso de error.
  """
  try:
    context.state["ending_session"] = True
    return {
      "result": "Success: La sesión ha sido marcada para finalizar de forma segura.",
      "agent_action": "Despídete cordialmente del cliente de forma muy breve y profesional, y finaliza la interacción."
    }
  except Exception as e:
    return {
      "result": f"Error: No se pudo marcar la sesión para finalizar: {str(e)}",
      "agent_action": "Informa al cliente de un inconveniente técnico leve, despídete y termina la llamada."
    }