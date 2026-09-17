//! PhotoCoop product identity.
//!
//! Keep Graphite patches limited to reading these constants so upstream merges
//! stay small. Do not put Graphite-specific message types in this crate.

pub const APP_NAME: &str = "PhotoCoop";
pub const ABOUT_TITLE: &str = "About PhotoCoop";
pub const ABOUT_HEADING: &str = "PhotoCoop is a Graphite fork";
pub const WEBSITE_URL: &str = "https://github.com/GraphiteEditor/Graphite";
pub const GRAPHITE_WEBSITE_URL: &str = "https://graphite.art";
pub const GRAPHITE_DONATE_URL: &str = "https://graphite.art/donate/";
pub const GRAPHITE_LEARN_URL: &str = "https://graphite.art/learn/";
pub const GRAPHITE_LICENSE_URL: &str = "https://graphite.art/license#source-code";

pub fn about_body(localized_commit_date: &str, localized_commit_year: &str) -> String {
	format!(
		"PhotoCoop adds independent branding, theme, and features on top of Graphite.\n\
		\n\
		Graphite engine {localized_commit_date}\n\
		Copyright © {localized_commit_year} Graphite contributors\n\
		PhotoCoop branding © PhotoCoop contributors"
	)
}

pub fn licenses_intro() -> &'static str {
	"PhotoCoop is a fork of Graphite. Graphite source code stays MIT OR Apache-2.0. PhotoCoop logos and icons are original and replace Graphite's proprietary branding."
}
