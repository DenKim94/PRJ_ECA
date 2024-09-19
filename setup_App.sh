#!/bin/bash

function print_message() {
    local COLOR=$1
    local MESSAGE=$2
    RESET="\033[0m"
    case $COLOR in
        "green")
            echo -e "\033[32m$MESSAGE$RESET"
            ;;
        "red")
            echo -e "\033[31m$MESSAGE$RESET"
            ;;
        *)
            echo "$MESSAGE"
            ;;
    esac
}

# 1. Python Installation überprüfen oder installieren
print_message "green" ">> Überprüfen, ob Python3 installiert ist..."

if ! command -v python3 &> /dev/null
then
    print_message "red" ">> Python3 ist nicht installiert. Installiere Python3 mit Homebrew..."
    
    # Überprüfen, ob Homebrew installiert ist
    if ! command -v brew &> /dev/null
    then
        print_message "red" ">> Homebrew ist nicht installiert. Installiere Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Installiere Python3
    brew install python
else
    print_message "green" ">> Python3 ist bereits installiert!"
fi

# 2. Python-Version
print_message "green" ">> Überprüfen der Python-Version..."
python3 --version

# 3. Installation von pip3
print_message "green" ">> Überprüfen, ob pip3 installiert ist..."

if ! command -v pip3 &> /dev/null
then
    print_message "red" ">> pip3 ist nicht installiert. Installiere pip3..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
else
    print_message "green" ">> pip3 ist bereits installiert!"
fi

# 4. Abhängigkeiten aus der requirements.txt installieren
if [ -f "requirements.txt" ]; then
    print_message "green" ">> Installiere Python-Module aus requirements.txt..."

    # Schleife durch die requirements.txt und installiere nur fehlende Pakete
    while IFS= read -r package
    do
        # Paketname und Version trennen (falls vorhanden)
        package_name=$(echo $package | cut -d'=' -f 1)

        # Prüfen, ob das Paket bereits installiert ist
        if ! pip3 show "$package_name" &> /dev/null
        then
            print_message "red" ">> Paket $package_name ist nicht installiert. Installiere $package..."
            pip3 install "$package"
        else
            print_message "green" ">> $package_name ist bereits installiert!"
        fi
    done < "requirements.txt"
	
	# Hinweis für den Benutzer nach Abschluss
	print_message "green" ">> Installation ist abgeschlossen! Sie können die Anwendung starten: ./runApp.sh"
	
else
    print_message "red" ">> requirements.txt nicht gefunden!"
fi
