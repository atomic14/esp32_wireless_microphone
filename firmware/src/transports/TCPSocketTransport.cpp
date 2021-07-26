#include <WiFiServer.h>
#include "TCPSocketTransport.h"

void TCPSocketTransport::begin()
{
  Serial.println("Connect to TCP socket microphone.local:9090 to try out TCP socket streaming");
  server = new WiFiServer(9090);
  server->begin();
}

void TCPSocketTransport::send(void *data, size_t len)
{
  // get any new connections
  WiFiClient client = server->available();
  if (client)
  {
    Serial.println("New Client");
    // add to the list of clients
    for (int i = 0; i < MAX_CLIENTS; i++)
    {
      if (NULL == clients[i])
      {
        clients[i] = new WiFiClient(client);
        break;
      }
    }
  }
  // send the audio data to any clients
  for (int i = 0; i < MAX_CLIENTS; i++)
  {
    if (clients[i] != NULL && (*clients[i]))
    {
      // send the samples to the client
      clients[i]->write((uint8_t *)data, len);
    }
    else
    {
      // client has gone away, remove it from the list
      clients[i] = NULL;
    }
  }
}