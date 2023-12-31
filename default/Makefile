###############################################################################
# Makefile for the project NetLoader
###############################################################################

## General Flags
PROJECT = NetLoader
GAME = NetLoader
MCU = atmega644
TARGET = $(GAME).elf
CC = avr-gcc
INFO=../gameinfo.properties
UZEBIN_DIR=../bin

## Kernel settings
KERNEL_DIR = ../kernel
KERNEL_OPTIONS  = -DVIDEO_MODE=3 -DINTRO_LOGO=1 -DSOUND_CHANNEL_4_ENABLE=0 -DSOUND_CHANNEL_5_ENABLE=0 -DSCROLLING=0 -DSOUND_MIXER=1
KERNEL_OPTIONS += -DMAX_SPRITES=0 -DRAM_TILES_COUNT=0 -DSCREEN_TILES_V=27 -DUART=1  -DUART_RX_BUFFER_SIZE=256 -DUART_TX_BUFFER_SIZE=128
#KERNEL_OPTIONS += -DVRAM_TILES_V=32

## Options common to compile, link and assembly rules
COMMON = -mmcu=$(MCU)

## Compile options common for all C compilation units.
CFLAGS = $(COMMON)
CFLAGS += -Wall -gdwarf-2 -std=gnu99 -DF_CPU=28636360UL -Os -fsigned-char -ffunction-sections -fno-toplevel-reorder
CFLAGS += -MD -MP -MT $(*F).o -MF dep/$(@F).d 
CFLAGS += $(KERNEL_OPTIONS)


## Assembly specific flags
ASMFLAGS = $(COMMON)
ASMFLAGS += $(CFLAGS)
ASMFLAGS += -x assembler-with-cpp -Wa,-gdwarf2

## Linker flags
LDFLAGS = $(COMMON)
LDFLAGS += -Wl,-Map=$(GAME).map 
LDFLAGS += -Wl,-gc-sections 
#LDFLAGS += -Wl,--section-start,.noinit=0x800100 -Wl,--section-start,.data=0x800500


## Intel Hex file production flags
HEX_FLASH_FLAGS = -R .eeprom

#HEX_EEPROM_FLAGS = -j .eeprom
#HEX_EEPROM_FLAGS += --set-section-flags=.eeprom="alloc,load"
#HEX_EEPROM_FLAGS += --change-section-lma .eeprom=0 --no-change-warnings


## Objects that must be built in order to link
#OBJECTS = uzeboxVideoEngineCore.o  uzeboxCore.o uzeboxSoundEngine.o uzeboxSoundEngineCore.o uzeboxVideoEngine.o spiram.o sdBase.o bootlib.o $(GAME).o
OBJECTS = uzeboxVideoEngineCore.o  uzeboxCore.o uzeboxSoundEngine.o uzeboxSoundEngineCore.o uzeboxVideoEngine.o uzenet.o bootlib.o $(GAME).o

## Objects explicitly added by the user
LINKONLYOBJECTS = 

## Include Directories
INCLUDES = -I"$(KERNEL_DIR)" 

## Build
all: ../data/tileset.inc $(TARGET) $(GAME).hex $(GAME).eep $(GAME).lss $(GAME).uze size

## Rebuild graphics ressource

## Compile Kernel files
uzeboxVideoEngineCore.o: $(KERNEL_DIR)/uzeboxVideoEngineCore.s
	$(CC) $(INCLUDES) $(ASMFLAGS) -c  $<

uzeboxSoundEngineCore.o: $(KERNEL_DIR)/uzeboxSoundEngineCore.s
	$(CC) $(INCLUDES) $(ASMFLAGS) -c  $<

uzeboxCore.o: $(KERNEL_DIR)/uzeboxCore.c
	$(CC) $(INCLUDES) $(CFLAGS) -c  $<

uzeboxSoundEngine.o: $(KERNEL_DIR)/uzeboxSoundEngine.c
	$(CC) $(INCLUDES) $(CFLAGS) -c  $<

uzeboxVideoEngine.o: $(KERNEL_DIR)/uzeboxVideoEngine.c
	$(CC) $(INCLUDES) $(CFLAGS) -c  $<

uzenet.o: ../uzenet.c
	$(CC) $(INCLUDES) $(CFLAGS) -c  $<

bootlib.o: $(KERNEL_DIR)/bootlib.s $(DIRS)
	$(CC) $(INCLUDES) $(ASMFLAGS) -c $< -o $@

## Compile game sources
$(GAME).o: ../$(GAME).c
	$(CC) $(INCLUDES) $(CFLAGS) -c  $<

##Link
$(TARGET): $(OBJECTS)
	 $(CC) $(LDFLAGS) $(OBJECTS) $(LINKONLYOBJECTS) $(LIBDIRS) $(LIBS) -o $(TARGET)

../data/tileset.inc: ../data/tileset.png ../data/tileset.xml
	$(UZEBIN_DIR)/gconvert ../data/tileset.xml

../data/spriteset.inc: ../data/spriteset.png ../data/spriteset.xml
	$(UZEBIN_DIR)/gconvert ../data/spriteset.xml

%.hex: $(TARGET)
	avr-objcopy -O ihex $(HEX_FLASH_FLAGS)  $< $@

%.eep: $(TARGET)
	-avr-objcopy $(HEX_EEPROM_FLAGS) -O ihex $< $@ || exit 0

%.lss: $(TARGET)
	avr-objdump -h -S $< > $@

%.uze: $(TARGET)
	-$(UZEBIN_DIR)/packrom $(GAME).hex $@ $(INFO)

UNAME := $(shell sh -c 'uname -s 2>/dev/null || echo not')
AVRSIZEFLAGS := -A ${TARGET}
ifneq (,$(findstring MINGW,$(UNAME)))
AVRSIZEFLAGS := -C --mcu=${MCU} ${TARGET}
endif

size: ${TARGET}
	@echo
	@avr-size ${AVRSIZEFLAGS}

## Clean target
.PHONY: clean flash read_flash emu
clean:
	-rm -rf ../data/tileset.inc ../data/spriteset.inc eeprom.bin $(OBJECTS) $(GAME).eep $(GAME).elf $(GAME).hex $(GAME).lss $(GAME).map $(GAME).o $(GAME).uze dep

flash: all
	$(AVRDUDE) -U flash:w:$(GAME).hex:i

read_flash:
	$(AVRDUDE) -U flash:r:$(GAME).bin:r

emu: all
	$(UZEBIN_DIR)/cuzebox $(GAME).uze


## Other dependencies
-include $(shell mkdir dep 2>/dev/null) $(wildcard dep/*)

