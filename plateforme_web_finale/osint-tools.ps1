# Script PowerShell pour Windows - Lance les outils OSINT dans le conteneur Docker
# Usage: .\osint-tools.ps1 <tool> <arguments>

param(
    [Parameter(Position=0)]
    [string]$Tool,

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Nom du conteneur Docker (à adapter si nécessaire)
$ContainerName = "plateforme_osint"

function Show-Help {
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                   🔍 OUTILS OSINT (Windows)                  ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\osint-tools.ps1 <outil> <arguments>"
    Write-Host ""
    Write-Host "OUTILS DISPONIBLES:" -ForegroundColor Yellow
    Write-Host "  sherlock    - Recherche d'username sur 300+ sites"
    Write-Host "  holehe      - Recherche d'email sur 120+ sites"
    Write-Host "  maigret     - Recherche avancée avec extraction de données"
    Write-Host ""
    Write-Host "EXEMPLES:" -ForegroundColor Yellow
    Write-Host "  .\osint-tools.ps1 sherlock johndoe"
    Write-Host "  .\osint-tools.ps1 holehe test@gmail.com"
    Write-Host "  .\osint-tools.ps1 holehe test@gmail.com --only-used"
    Write-Host "  .\osint-tools.ps1 maigret johndoe"
    Write-Host ""
    Write-Host "COMMANDES SPÉCIALES:" -ForegroundColor Yellow
    Write-Host "  .\osint-tools.ps1 test       - Tester tous les outils"
    Write-Host "  .\osint-tools.ps1 shell      - Ouvrir un shell dans le conteneur"
    Write-Host "  .\osint-tools.ps1 containers - Lister les conteneurs Docker"
    Write-Host ""
}

function Test-Tools {
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                   🧪 TEST DES OUTILS                         ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""

    $bashScript = "/home/user/Plateforme_OSINT/plateforme_web_finale/osint-tools.sh"
    docker exec -it $ContainerName bash -c "source /home/user/osint-venv/bin/activate && $bashScript test"
}

function Show-Containers {
    Write-Host "📦 Conteneurs Docker en cours d'exécution:" -ForegroundColor Cyan
    Write-Host ""
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
    Write-Host ""
    Write-Host "💡 Conseil: Si ton conteneur n'apparaît pas, essaie:" -ForegroundColor Yellow
    Write-Host "   docker ps -a    # Voir tous les conteneurs (même arrêtés)"
    Write-Host ""
}

function Open-Shell {
    Write-Host "🐚 Ouverture d'un shell dans le conteneur..." -ForegroundColor Cyan
    Write-Host "   Tapez 'exit' pour sortir" -ForegroundColor Gray
    Write-Host ""
    docker exec -it $ContainerName bash
}

function Invoke-OsintTool {
    param(
        [string]$ToolName,
        [string[]]$Args
    )

    # Construire la commande
    $argsString = ($Args -join ' ')
    $command = "source /home/user/osint-venv/bin/activate && $ToolName $argsString"

    Write-Host "🔍 Lancement de $ToolName..." -ForegroundColor Cyan
    Write-Host ""

    # Exécuter dans le conteneur
    docker exec -it $ContainerName bash -c $command
}

# Gestion des arguments
switch ($Tool.ToLower()) {
    "" {
        Show-Help
    }
    "help" {
        Show-Help
    }
    "--help" {
        Show-Help
    }
    "-h" {
        Show-Help
    }
    "test" {
        Test-Tools
    }
    "containers" {
        Show-Containers
    }
    "shell" {
        Open-Shell
    }
    "sherlock" {
        Invoke-OsintTool -ToolName "sherlock" -Args $Arguments
    }
    "holehe" {
        Invoke-OsintTool -ToolName "holehe" -Args $Arguments
    }
    "maigret" {
        Invoke-OsintTool -ToolName "maigret" -Args $Arguments
    }
    default {
        Write-Host "❌ Outil inconnu: $Tool" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}
