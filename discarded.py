def render_contact_sheet_magick(photos: Sequence[Path | str], regions: ContactRegions, out_file: Path | str):
    args = ['magick', '-size', f'{regions.sheet_width}x{regions.sheet_height}', 'canvas:none']
    for file_name, region in zip(photos, regions.regions):
        # Warning: File name is unescaped, this wouldn't fly with untrusted input!
        # Worringly, I cannot find any documentation on how to escape file names
        # inside a -draw command in ImageMagick.
        cmd = f"image SrcOver {region.x},{region.y} {region.w},{region.h} '{file_name}'"
        args += ['-draw', cmd, '-virtual-pixel', 'Edge']
    args.append(str(out_file))
    subprocess.check_call(args)