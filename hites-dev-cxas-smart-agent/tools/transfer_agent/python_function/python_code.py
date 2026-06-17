def transfer_agent(queue: str = "", channel: str = "") -> str:
  context.variables["transferring_to_agent"] = True 
  if queue:
      context.variables["queue"] = queue
  
  # Always prefer the channel already in the session if it exists, because the LLM often guesses "voice" incorrectly.
  session_channel = str(context.variables.get('channel', '')).lower()
  
  if session_channel:
      final_channel = session_channel
  else:
      final_channel = channel.lower() or 'voice'
      context.variables["channel"] = final_channel

  transferring_to_agent = context.variables.get('transferring_to_agent', '')
  queue = context.variables.get('queue', '')
  
  if transferring_to_agent:
    print(f"transferring_to_agent to queue: {queue} on channel: {final_channel}")
    
    is_chat = "chat" in final_channel or "conversación" in final_channel or "conversacion" in final_channel or "text" in final_channel

    if is_chat:
        mapping = {
            "CentroFinancieroTelefonico": 92,
            "Atencion general": 92,
            "Atención general": 92,
            "Seguros": 93,
            "Despacho_Retiro": 94,
            "Cambio_Devol_SSTT_armado": 95,
            "Sac_Cobranzas": 96
        }
        menu_id = mapping.get(queue, 92)
    else:
        mapping = {
            "CentroFinancieroTelefonico": 38,
            "Atencion general": 38,
            "Atención general": 38,
            "Seguros": 39,
            "Despacho_Retiro": 56,
            "Cambio_Devol_SSTT_armado": 57,
            "Sac_Cobranzas": 58
        }
        menu_id = mapping.get(queue, 38)
    
    payload = {
      "ujet": {
        "escalation_reason": "by_virtual_agent",
        "type": "action",
        "sip_parameters": {
          "x-session-id": context.variables.get('session_id', 'no-Tengo-Session_ID'),
          "x-headers": {
            "transfer-call": "Callback before LLM",
            "header-1": context.variables.get('session_id', 'no-Tengo-Session_ID'),
            "sessionid": context.variables.get('session_id', 'no-Tengo-Session_ID')
          }
        },
        "action": "escalation",
        "menu_id": menu_id
      }
    }
    
    if is_chat:
        print(f"Chat handoff triggered. TELEPHONY_PAYLOAD is : {payload}")
        context.variables["TELEPHONY_PAYLOAD"] = payload
    else:
        print(f"Voice handoff triggered. TELEPHONY_PAYLOAD is : {payload}")
        context.variables["TELEPHONY_PAYLOAD"] = payload

  return "Success"
