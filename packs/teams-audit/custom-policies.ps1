# Read: users with a direct meeting, messaging or calling policy assignment
# (empty = the org-wide Global policy applies).
param($Mode, $Inputs, $Change)

Get-CsOnlineUser -ResultSize 10000 | Where-Object {
    $_.TeamsMeetingPolicy -or $_.TeamsMessagingPolicy -or $_.TeamsCallingPolicy
} | ForEach-Object {
    @{
        user      = [string]$_.UserPrincipalName
        meeting   = "$($_.TeamsMeetingPolicy)"
        messaging = "$($_.TeamsMessagingPolicy)"
        calling   = "$($_.TeamsCallingPolicy)"
    }
}
