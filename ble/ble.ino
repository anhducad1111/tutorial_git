#include <NimBLEDevice.h>
#include <NimBLEUtils.h>
#include <NimBLEServer.h>
#include <time.h>

// UUID definitions
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define TIMESTAMP_UUID "7AE63A01-7AD5-464B-803D-8A392D242CC7"
#define IMU1_UUID "55A58E5B-9F51-47DC-B6C7-EE929BA79664"
#define IMU2_UUID "84b70b01-8869-4a23-ab4f-fbfd1a25a925"

// Struct for IMU data (9 x int16_t = 18 bytes)
struct ImuData {
    int16_t accel[3];  // X, Y, Z in mg
    int16_t gyro[3];   // X, Y, Z in 1/100th rad/s
    int16_t mag[3];    // X, Y, Z in uT
};

bool deviceConnected = false;
static NimBLEServer* pServer = nullptr;
static NimBLECharacteristic* pTimestampChar = nullptr;
static NimBLECharacteristic* pImu1Char = nullptr;
static NimBLECharacteristic* pImu2Char = nullptr;

unsigned long lastImu1Update = 0;
unsigned long lastImu2Update = 0;

// Class quản lý callback cho Server
class ServerCallbacks: public NimBLEServerCallbacks {
    void onConnect(NimBLEServer* pServer, NimBLEConnInfo& connInfo) override {
        deviceConnected = true;
        Serial.println("Client connected");
    };

    void onDisconnect(NimBLEServer* pServer, NimBLEConnInfo& connInfo, int reason) override {
        deviceConnected = false;
        Serial.println("Client disconnected");
        NimBLEDevice::startAdvertising();
    }
};

// Class quản lý callback cho TimestampCharacteristic
class TimestampCallbacks: public NimBLECharacteristicCallbacks {
    void onWrite(NimBLECharacteristic* pCharacteristic, NimBLEConnInfo& connInfo) override {
        std::string value = pCharacteristic->getValue();
        if (value.length() == 8) {
            uint64_t timestamp;
            memcpy(&timestamp, value.data(), 8);
            // Set system time
            timeval tv = { (time_t)timestamp, 0 };
            settimeofday(&tv, NULL);
        }
    }
};

// Generate random IMU data in proper ranges
ImuData generateRandomImuData() {
    ImuData data;
    
    // Accelerometer: ±2g (±2000mg)
    for(int i = 0; i < 3; i++) {
        data.accel[i] = random(-2000, 2000);  // mg
    }
    
    // Gyroscope: ±2 rad/s (±200 in 1/100th rad/s)
    for(int i = 0; i < 3; i++) {
        data.gyro[i] = random(-200, 200);  // 1/100th rad/s
    }
    
    // Magnetometer: ±50 uT
    for(int i = 0; i < 3; i++) {
        data.mag[i] = random(-50, 50);  // uT
    }
    
    return data;
}

void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE Server...");

    // Initialize BLE
    NimBLEDevice::init("ESP32-ad");
    NimBLEDevice::setPower(ESP_PWR_LVL_P9);

    // Create server
    pServer = NimBLEDevice::createServer();
    pServer->setCallbacks(new ServerCallbacks());

    // Create service
    NimBLEService* pService = pServer->createService(SERVICE_UUID);

    // Create characteristics
    pTimestampChar = pService->createCharacteristic(
        TIMESTAMP_UUID,
        NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::WRITE
    );
    pTimestampChar->setCallbacks(new TimestampCallbacks());

    pImu1Char = pService->createCharacteristic(
        IMU1_UUID,
        NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
    );

    pImu2Char = pService->createCharacteristic(
        IMU2_UUID,
        NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
    );

    // Initialize timestamp
    uint64_t currentTime = time(nullptr);
    pTimestampChar->setValue((uint8_t*)&currentTime, 8);

    // Initialize IMU values with random data
    ImuData imu1Data = generateRandomImuData();
    ImuData imu2Data = generateRandomImuData();
    pImu1Char->setValue((uint8_t*)&imu1Data, sizeof(ImuData));
    pImu2Char->setValue((uint8_t*)&imu2Data, sizeof(ImuData));

    // Start service
    pService->start();

    // Setup advertising
    NimBLEAdvertising* pAdvertising = NimBLEDevice::getAdvertising();
    pAdvertising->setName("ESP32-ad");
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->enableScanResponse(true);
    pAdvertising->start();
    
    Serial.println("BLE server ready");
}

void updateImu1() {
    if (millis() - lastImu1Update >= 3000) {
        // Generate new random IMU data
        ImuData imuData = generateRandomImuData();

        // Set and notify
        pImu1Char->setValue((uint8_t*)&imuData, sizeof(ImuData));
        if (deviceConnected) {
            pImu1Char->notify();
        }
        lastImu1Update = millis();

        // Debug print
        Serial.println("IMU1 Data:");
        Serial.printf("Accel: X=%d Y=%d Z=%d (mg)\n", 
            imuData.accel[0], imuData.accel[1], imuData.accel[2]);
        Serial.printf("Gyro: X=%d Y=%d Z=%d (0.01 rad/s)\n",
            imuData.gyro[0], imuData.gyro[1], imuData.gyro[2]);
        Serial.printf("Mag: X=%d Y=%d Z=%d (uT)\n",
            imuData.mag[0], imuData.mag[1], imuData.mag[2]);
    }
}

void updateImu2() {
    if (millis() - lastImu2Update >= 5000) {
        // Generate new random IMU data
        ImuData imuData = generateRandomImuData();

        // Set and notify
        pImu2Char->setValue((uint8_t*)&imuData, sizeof(ImuData));
        if (deviceConnected) {
            pImu2Char->notify();
        }
        lastImu2Update = millis();

        // Debug print
        Serial.println("IMU2 Data:");
        Serial.printf("Accel: X=%d Y=%d Z=%d (mg)\n", 
            imuData.accel[0], imuData.accel[1], imuData.accel[2]);
        Serial.printf("Gyro: X=%d Y=%d Z=%d (0.01 rad/s)\n",
            imuData.gyro[0], imuData.gyro[1], imuData.gyro[2]);
        Serial.printf("Mag: X=%d Y=%d Z=%d (uT)\n",
            imuData.mag[0], imuData.mag[1], imuData.mag[2]);
    }
}

void updateTimestamp() {
    if (deviceConnected) {
        uint64_t currentTime = time(nullptr);
        pTimestampChar->setValue((uint8_t*)&currentTime, 8);
    }
}

void loop() {
    if (deviceConnected) {
        updateTimestamp();
        updateImu1();
        updateImu2();
    }
    delay(10);
}
