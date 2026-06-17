def cortar_llamada_mmr(reason: str) -> str:
  if reason == 'csat':
    context.variables["TELEPHONY_PAYLOAD"] = {
      "ujet": {
        "type": "action",
        "action": "end"
      }
    }
    return "Success"
  elif reason == 'end':
    context.variables["TELEPHONY_PAYLOAD"] = {
      "ujet": {
        "type": "action",
        "action": "end"
      }
    }
    return "Success"   
  else:
    context.variables["TELEPHONY_PAYLOAD"] = {
      "ujet": {
        "type": "action",
        "action": "end"
      }
    }
    return None