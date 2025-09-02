FROM alpine:latest

# Install Lua 5.3, LuaRocks, and build tools
RUN apk add --no-cache \
      lua5.3 lua5.3-dev luarocks5.3 \
      gcc g++ make musl-dev \
    && luarocks-5.3 install luasocket \
    && luarocks-5.3 install dkjson

WORKDIR /app
COPY server.lua .

EXPOSE 8765
CMD ["lua5.3", "server.lua"]