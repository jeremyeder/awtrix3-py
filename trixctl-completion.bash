#!/bin/bash
# Bash completion for trixctl
# 
# Installation:
#   # System-wide (requires sudo):
#   sudo cp trixctl-completion.bash /etc/bash_completion.d/trixctl
#
#   # User-specific:
#   mkdir -p ~/.bash_completion.d
#   cp trixctl-completion.bash ~/.bash_completion.d/trixctl
#   echo 'source ~/.bash_completion.d/trixctl' >> ~/.bashrc

_trixctl_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Global options
    opts="--host --username --password --generate-config --help"
    
    # Commands
    commands="notify stats power app sound"
    
    # If we're completing the first argument after trixctl
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "${opts} ${commands}" -- ${cur}) )
        return 0
    fi
    
    # Handle options that need values
    case "${prev}" in
        --host)
            # Complete with common IP patterns (user can override)
            COMPREPLY=( $(compgen -W "192.168.1.100 192.168.0.100 localhost" -- ${cur}) )
            return 0
            ;;
        --username)
            COMPREPLY=( $(compgen -W "admin user" -- ${cur}) )
            return 0
            ;;
        --password)
            # Don't complete passwords
            return 0
            ;;
    esac
    
    # Handle subcommands
    case "${COMP_WORDS[1]}" in
        power)
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=( $(compgen -W "on off" -- ${cur}) )
            fi
            ;;
        notify|app|sound)
            # These commands take text arguments - no specific completion
            ;;
        stats)
            # stats takes no arguments
            ;;
        *)
            # Default to global options
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
    esac
}

# Register the completion function
complete -F _trixctl_completion trixctl