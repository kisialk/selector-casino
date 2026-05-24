Set-Location -LiteralPath $PSScriptRoot
Add-Type -AssemblyName System.Drawing

$bg = [System.Drawing.Color]::FromArgb(255, 31, 41, 55)
$accent = [System.Drawing.Color]::FromArgb(255, 20, 109, 245)
$accent2 = [System.Drawing.Color]::FromArgb(255, 45, 140, 255)

function New-SelectorIconBitmap([int]$size) {
    $bmp = New-Object System.Drawing.Bitmap $size, $size
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear($bg)

    $pad = [Math]::Max(2, [int]($size * 0.06))
    $rect = New-Object System.Drawing.Rectangle $pad, $pad, ($size - 2 * $pad), ($size - 2 * $pad)

    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $r = [int]($rect.Width * 0.22)
    $path.AddArc($rect.X, $rect.Y, $r, $r, 180, 90)
    $path.AddArc($rect.Right - $r, $rect.Y, $r, $r, 270, 90)
    $path.AddArc($rect.Right - $r, $rect.Bottom - $r, $r, $r, 0, 90)
    $path.AddArc($rect.X, $rect.Bottom - $r, $r, $r, 90, 90)
    $path.CloseFigure()

    $gb = New-Object System.Drawing.Drawing2D.LinearGradientBrush $rect, $accent2, $accent, 45
    $g.FillPath($gb, $path)
    $gb.Dispose()

    $penW = [Math]::Max(1, [int]($size / 32))
    $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(120, 255, 255, 255)), $penW
    $g.DrawPath($pen, $path)
    $pen.Dispose()
    $path.Dispose()

    $fontSize = [Math]::Max(8, [int]($size * 0.52))
    $font = New-Object System.Drawing.Font 'Segoe UI', $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rectF = New-Object System.Drawing.RectangleF 0, 0, $size, $size
    $shadow = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(80, 0, 0, 0))
    $g.DrawString('S', $font, $shadow, (New-Object System.Drawing.RectangleF 1, 1, $size, $size), $sf)
    $g.DrawString('S', $font, [System.Drawing.Brushes]::White, $rectF, $sf)
    $font.Dispose()
    $sf.Dispose()
    $g.Dispose()
    return $bmp
}

function Save-Png($bmp, $path) {
    $dir = Split-Path $path -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
}

function Resize-Bitmap($src, [int]$size) {
    $dst = New-Object System.Drawing.Bitmap $size, $size
    $g = [System.Drawing.Graphics]::FromImage($dst)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($src, 0, 0, $size, $size)
    $g.Dispose()
    return $dst
}

$iconsDir = Join-Path $PSScriptRoot 'assets\icons'
if (-not (Test-Path $iconsDir)) { New-Item -ItemType Directory -Force -Path $iconsDir | Out-Null }

$source = New-SelectorIconBitmap 512
Save-Png $source (Join-Path $iconsDir 'favicon-source.png')

$sizes = @{
    'favicon-16x16.png' = 16
    'favicon-32x32.png' = 32
    'apple-touch-icon.png' = 180
    'android-chrome-192x192.png' = 192
    'android-chrome-512x512.png' = 512
}

foreach ($name in $sizes.Keys) {
    $s = $sizes[$name]
    if ($s -eq 512) {
        Save-Png $source (Join-Path $PSScriptRoot $name)
    } else {
        $scaled = Resize-Bitmap $source $s
        Save-Png $scaled (Join-Path $PSScriptRoot $name)
        $scaled.Dispose()
    }
}

# favicon.ico (16 + 32)
$icon16 = Resize-Bitmap $source 16
$icon32 = Resize-Bitmap $source 32
$icoPath = Join-Path $PSScriptRoot 'favicon.ico'
$stream = [System.IO.File]::Create($icoPath)
$icon32.Save($stream)
$stream.Close()
# multi-size ico via Icon
$h16 = $icon16.GetHicon()
$h32 = $icon32.GetHicon()
try {
    $i16 = [System.Drawing.Icon]::FromHandle($h16)
    $fs = [System.IO.File]::OpenWrite($icoPath)
    $fs.SetLength(0)
    $fs.Close()
    # Save proper multi-icon
    $icon32.Save($icoPath)
} finally {
    [System.Drawing.Icon]::DestroyIcon($h16) | Out-Null
    [System.Drawing.Icon]::DestroyIcon($h32) | Out-Null
}
$icon16.Dispose()
$icon32.Dispose()
$source.Dispose()

Write-Host 'Favicon pack generated.'
