-- server.lua
-- luarocks install luasocket
-- luarocks install dkjson (optional for JSON decoding)

local socket = require("socket")
local has_json, json = pcall(require, "dkjson")

local host, port = "0.0.0.0", 8765
local server = assert(socket.bind(host, port))
server:settimeout(0) -- non-blocking

print(("Lua server listening on %s:%d"):format(host, port))

local client
while true do
  if not client then
    client = server:accept()
    if client then
      client:settimeout(0)
      print("Client connected")
    end
  else
    local line, err = client:receive("*l")
    if line then
      if has_json then
        local obj, pos, jerr = json.decode(line, 1, nil)
        if obj then
          print(("[RX] intent=%s args=%s"):format(obj.intent, json.encode(obj.args)))
        else
          print("[RX] JSON decode error:", jerr, " raw:", line)
        end
      else
        print("[RX] raw:", line)
      end
    elseif err == "closed" then
      print("Client disconnected")
      client:close()
      client = nil
    end
  end
  socket.sleep(0.01)
end