#pragma once
#include "Transport.h"

class WiFiClient;
class WiFiServer;
#define MAX_CLIENTS 10

class TCPSocketTransport : public Transport
{
private:
  WiFiServer *server = NULL;
  WiFiClient *clients[MAX_CLIENTS] = {NULL};

public:
  void begin();
  void send(void *data, size_t size) override;
};