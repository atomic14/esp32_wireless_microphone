#pragma once

class Transport;
class I2SSampler;

class Application
{
private:
  Transport *transport1 = NULL;
  Transport *transport2 = NULL;
  I2SSampler *input = NULL;

public:
  void begin();
  static void streamer_task(void *param);
};