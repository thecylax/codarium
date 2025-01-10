SRC_DIR = src
BUILD_DIR = build
MANIFEST = com.blacktomato.codarium.json

MAIN_PY = $(SRC_DIR)/main.py
EXECUTABLE = $(BUILD_DIR)/src/codarium

all: build run

flatpak_build:
	flatpak-builder --install-deps-from=flathub dist $(MANIFEST)

flatpak_run:
	flatpak-builder --run build-dir org.flatpak.Hello.json hello.sh

setup:
	meson setup build

build: check_build_dir
	meson compile -C build

check_build_dir:
	@if [ ! -d $(BUILD_DIR) ]; then \
		$(MAKE) setup; \
	fi

install: build
	meson install -C build

run: install
	python $(EXECUTABLE)

frun:
	python $(EXECUTABLE)