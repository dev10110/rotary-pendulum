using BaremetalPi

init_spi("/dev/spidev0.0", mode=BaremetalPi.SPI_MODE_1)

function read()
  rx_buf = [0x00, 0x00]
  
  spi_transfer!(1, [0x00,0x00], rx_buf)
  
  l, r = rx_buf
  
  s = ((( l & 0xFFFF) << 8)  | (r & 0x00FF)) & ~0xC000

  return 180*(s/8192-1)
end



while true
 println(read())
end


