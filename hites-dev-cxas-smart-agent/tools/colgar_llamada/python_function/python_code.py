def colgar_llamada(reason: str) -> str:
  context.state["ending_session"] = True
  context.variables["TELEPHONY_PAYLOAD"] = {
    "ujet": {
      "type": "action",
      "action": "end"
    }
  }
  return "Success"