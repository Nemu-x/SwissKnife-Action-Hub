# Read: distribution lists without a single member.
param($Mode, $Inputs, $Change)

Get-DistributionGroup -ResultSize Unlimited | ForEach-Object {
    $members = @(Get-DistributionGroupMember -Identity ([string]$_.PrimarySmtpAddress) -ResultSize 1)
    if ($members.Count -eq 0) {
        @{
            name      = [string]$_.DisplayName
            address   = [string]$_.PrimarySmtpAddress
            managedBy = ($_.ManagedBy | ForEach-Object { "$_" }) -join ', '
        }
    }
}
