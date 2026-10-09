# Read: every Full Access grant on a shared mailbox (not inherited, not system).
param($Mode, $Inputs, $Change)

Get-Mailbox -RecipientTypeDetails SharedMailbox -ResultSize Unlimited | ForEach-Object {
    $box = [string]$_.PrimarySmtpAddress
    Get-MailboxPermission -Identity $box | Where-Object {
        -not $_.IsInherited -and -not $_.Deny -and "$($_.User)" -notlike 'NT AUTHORITY*' -and "$($_.User)" -notlike 'S-1-5-*'
    } | ForEach-Object {
        @{
            mailbox = $box
            user    = "$($_.User)"
            rights  = ($_.AccessRights | ForEach-Object { "$_" }) -join ', '
        }
    }
}
