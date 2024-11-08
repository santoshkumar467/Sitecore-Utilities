#Admin account pwds shouldn't be reset
$adminUsers = @('sitecore\ServicesAPI', 'sitecore\Admin','sitecore\coveouser')

$userInfo = @()
$pwdStr = '_TempPwd@01'
 
#Filter Sitecore domain users.. If you custom domains, you can also filter through it.
Get-User -Filter "sitecore\*" | ForEach-Object{
    if($adminUsers -notcontains $_.Name){
        #New PWD EMAILID + SALT
        $newPWD = $_.Profile.Email.Split('@')[0] + $pwdStr
        #Reseting New Pwd
        $_ | Set-UserPassword -NewPassword $newPWD -Reset
        #Custom Object to export it
        $userInfo += @{Name =  $_.Name; Email =$_.Profile.Email;Pwd = $newPWD}
        Write-Host $_.Name, $_.Profile.Email, $newPWD
    }
     
}
 
#Custom Object to export it
$props = @{
        Title = "Password Information"
        InfoTitle = "Total $($userInfo.Count) items found!"
        InfoDescription = "The passwords for the following users have been reset."
        PageSize = 2500
    }
    [string[]] $columns = "Name"
    [string[]] $columns +=  "Email"
    [string[]] $columns +=  "Pwd"
     
    $userInfo | Show-ListView @props -Property $columns
