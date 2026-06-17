def escalate_to_agent(reason: str) -> str:  
  context.variables["TELEPHONY_PAYLOAD"] = {
        "ujet": {
          "deflection_type": "sip",
          "sip_uri": "sips:38@des-ccai-qitu0xq-tp-ujet.sip.sao-paulo.twilio.com",
          "action": "deflection",
          "type": "action"
        }
    }
  return "Success"
