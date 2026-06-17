def hangup() -> None:
  context.variables["TELEPHONY_PAYLOAD"] = {
    "ujet": {
      "session_variable": {
        "hangup": True
      },
      "action": "end",
      "type": "action"
    }
  }