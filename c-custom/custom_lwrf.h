#ifndef CUSTOM_LWRF_XX
#define CUSTOM_LWRF_XX

//Interface commands for LWRF Pigpio gpioCustom_2
#define CUSTOM_LWRF 7287
#define CUSTOM_LWRF_TX_INIT   1
#define CUSTOM_LWRF_TX_BUSY   2
#define CUSTOM_LWRF_TX_PUT    3
#define CUSTOM_LWRF_TX_CANCEL 4
#define CUSTOM_LWRF_RX_INIT   10
#define CUSTOM_LWRF_RX_CLOSE  11
#define CUSTOM_LWRF_RX_READY  12
#define CUSTOM_LWRF_RX_GET    13
#define CUSTOM_LWRF_TX_DEBUG  99
#define CUSTOM_LWRF_RX_DEBUG  100

#define CUSTOM_PROTO_LWRF     0
#define CUSTOM_PROTO_GAZCO    1

//Lightwave constants, some used for all protocols
#define LWRF_MSGLEN 10
#define LWRF_MAXMESSAGES 16
#define LWRF_MAXREPEAT 25
#define LWRX_MSG_TIMEOUT 1000000

#define LWRX_STATE_IDLE 0
#define LWRX_STATE_MSGSTARTFOUND 1
#define LWRX_STATE_BYTESTARTFOUND 2
#define LWRX_STATE_GETBYTE 3

#define LWTX_HIGH 280
#define LWTX_LOW 980
#define LWTX_GAP 10800

// defines for GAZCO
#define GAZCO_MSGLEN 6
#define GAZCO_TX_TRAIN1 400
#define GAZCO_TX_TRAIN2 500
#define GAZCO_TX_SHORT 320
#define GAZCO_TX_LONG 580
#define GAZCO_TX_GAP 20000

/* 
For transmitting LW messages
*/
int lwtxGpio;
char lwtxDebug[64];

int lwTxPut(char* msg, char repeat);
int gazcoTxPut(char* msg, char repeat);

/*
Receives from a 433MHz RX and tries to decode LWRF messages
*/
int lwrxGpio, lwrxRepeat;
char lwrxMsgQueue[LWRF_MAXMESSAGES][LWRF_MSGLEN + 1];
int lwrxQueueHead;
int lwrxQueueTail;
char lwrxMessage[LWRF_MSGLEN + 1];
int lwrxData, lwrxByte, lwrxBit, lwrxState, lwrxDuplicate, lwrxRepeatCount;
uint32_t lwrxLastTick, lwrxLastMessageTick;
char lwrxDebug[64];

void _lwrxCallback(int gpio, int level, uint32_t tick);
int lwrxQueueSize();
#endif

