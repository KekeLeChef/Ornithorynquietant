output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)
filenames = []
for hour_idx, T in enumerate(T_sur_24h, start=1):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    temp_dans_csv(T, x, y, z, ax, shapes, mappable, cbar)
    ax.set_title(f"Heure {hour_idx:02d}")
    fname = f"{output_dir}/frame_{hour_idx:02d}.png"
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close(fig)
    filenames.append(fname)
images = [imageio.imread(fname) for fname in filenames]
imageio.mimsave("temperature_24h.gif", images, duration=1.0)
print("GIF généré : temperature_24h.gif")c