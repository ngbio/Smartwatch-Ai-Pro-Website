export function optimizeCloudinaryImage(url, width = 640) {
  if (!url || !url.includes("res.cloudinary.com") || !url.includes("/upload/"))
    return url || "";

  const transform = `f_auto,q_auto:eco,w_${width},c_fill,g_auto`;
  return url.replace("/upload/", `/upload/${transform}/`);
}

export function buildCloudinarySrcSet(url, widths = [320, 480, 640]) {
  if (!url || !url.includes("res.cloudinary.com"))
    return "";

  return widths
    .map(width => `${optimizeCloudinaryImage(url, width)} ${width}w`)
    .join(", ");
}
