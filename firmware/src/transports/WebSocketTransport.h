#pragma once
#include "Transport.h"

class AsyncWebServer;
class AsyncWebSocket;
class AsyncWebSocketClient;

class WebSocketTransport : public Transport
{
private:
  AsyncWebServer *server = NULL;
  AsyncWebSocket *ws = NULL;
  // allow for one client at a time
  AsyncWebSocketClient *connected_client = NULL;

public:
  void begin();
  void send(void *data, size_t size) override;
};