# Read: user and shared mailboxes whose mailbox auditing is turned off.
param($Mode, $Inputs, $Change)

Get-Mailbox -ResultSize Unlimited | Where-Object { -not $_.AuditEnabled } | ForEach-Object {
    @{
        name    = [string]$_.DisplayName
        address = [string]$_.PrimarySmtpAddress
        type    = [string]$_.RecipientTypeDetails
    }
}
