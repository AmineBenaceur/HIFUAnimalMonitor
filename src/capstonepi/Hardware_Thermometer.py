import board
import busio
import adafruit_mcp9600
i2c = busio.I2C(board.SCL, board.SDA, frequency=10000)
mcp = adafruit_mcp9600.MCP9600(i2c)
print(mcp.temperature)
