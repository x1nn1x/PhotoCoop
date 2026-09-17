use crate::cmd::prelude::*;
use crate::{Error, workspace_dir};

const INFO_FILE: &str = ".branding";
const DIR: &str = "branding";
const MARQUEE_ICON: &str = "assets/icon-24px-two-tone/general-marquee-tool.svg";

pub fn setup() -> Result<(), Error> {
	let workspace = workspace_dir();
	let info_path = workspace.join(INFO_FILE);
	let dir_path = workspace.join(DIR);
	let marker_path = dir_path.join(INFO_FILE);

	let info = std::fs::read_to_string(&info_path).map_err(|e| Error::Io(e, format!("reading '{}'", info_path.display())))?;

	if let Ok(marker) = std::fs::read_to_string(&marker_path)
		&& marker == info
		&& dir_path.join(MARQUEE_ICON).is_file()
	{
		return Ok(());
	}

	let mut lines = info.lines().map(str::trim).filter(|l| !l.is_empty());
	let url = lines
		.next()
		.ok_or_else(|| Error::Io(std::io::Error::other("missing URL"), format!("parsing '{}'", info_path.display())))?;
	let sha256 = lines
		.next()
		.ok_or_else(|| Error::Io(std::io::Error::other("missing SHA-256"), format!("parsing '{}'", info_path.display())))?;

	eprintln!("Downloading branding assets from <{url}>...");

	if dir_path.exists() {
		std::fs::remove_dir_all(&dir_path).map_err(|e| Error::Io(e, format!("removing '{}'", dir_path.display())))?;
	}

	utils::internal("download").args([url, sha256, DIR, "--extract", "--strip", "1"]).dir(&workspace).run()?;

	std::fs::copy(&info_path, &marker_path).map_err(|e| Error::Io(e, format!("writing '{}'", marker_path.display())))?;

	// PHOTOCOOP-HOOK: Graphite has no marquee icon yet; copy only that extra file.
	let marquee_src = workspace.join("photocoop/branding").join(MARQUEE_ICON);
	let marquee_dst = dir_path.join(MARQUEE_ICON);
	if marquee_src.is_file() {
		if let Some(parent) = marquee_dst.parent() {
			std::fs::create_dir_all(parent).map_err(|e| Error::Io(e, format!("creating '{}'", parent.display())))?;
		}
		std::fs::copy(&marquee_src, &marquee_dst).map_err(|e| Error::Io(e, format!("copying '{}'", marquee_dst.display())))?;
	}

	Ok(())
}
