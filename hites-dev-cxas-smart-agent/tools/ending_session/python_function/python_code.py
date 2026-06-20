def ending_session() -> dict:
  """
  Establece la bandera de finalización de sesión en el estado de la llamada.
  Retorna un diccionario estructurado indicando el éxito o instruyendo al agente en caso de error.
  """
  try:
    context.state["ending_session"] = True
    return {
      "result": "Success: La sesión ha sido marcada para finalizar de forma segura.",
      "agent_action": "Llama de inmediato a la herramienta transfer_to_agent(agent_name='Maria_Root_Agent') de forma 100% silenciosa para retornar el control al orquestador, sin generar ningún texto o voz en tu respuesta."
    }
  except Exception as e:
    return {
      "result": f"Error: No se pudo marcar la sesión para finalizar: {str(e)}",
      "agent_action": "Llama de inmediato a la herramienta transfer_to_agent(agent_name='Maria_Root_Agent') de forma 100% silenciosa para retornar el control al orquestador."
    }