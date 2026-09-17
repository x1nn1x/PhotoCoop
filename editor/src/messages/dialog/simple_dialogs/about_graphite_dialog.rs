use crate::messages::layout::utility_types::widget_prelude::*;
use crate::messages::prelude::*;

/// A dialog for displaying information on [BuildMetadata] viewable via *Help* > *About Graphite* in the menu bar.
pub struct AboutGraphiteDialog {
	pub localized_commit_date: String,
	pub localized_commit_year: String,
}

impl DialogLayoutHolder for AboutGraphiteDialog {
	const ICON: &'static str = "GraphiteLogo";
	// PHOTOCOOP-HOOK
	const TITLE: &'static str = photocoop_identity::ABOUT_TITLE;

	fn layout_buttons(&self) -> Layout {
		let widgets = vec![TextButton::new("OK").emphasized(true).on_update(|_| FrontendMessage::DialogClose.into()).widget_instance()];

		Layout(vec![LayoutGroup::row(widgets)])
	}

	fn layout_column_2(&self) -> Layout {
		let links = [
			("Heart", "Donate to Graphite", photocoop_identity::GRAPHITE_DONATE_URL),
			("GraphiteLogo", "Graphite Website", photocoop_identity::GRAPHITE_WEBSITE_URL),
			("Volunteer", "Volunteer", "https://graphite.art/volunteer/"),
			("Credits", "Credits", "https://github.com/GraphiteEditor/Graphite/graphs/contributors"),
		];
		let mut widgets = links
			.into_iter()
			.map(|(icon, label, url)| {
				TextButton::new(label)
					.icon(icon)
					.flush(true)
					.on_update(|_| FrontendMessage::TriggerVisitLink { url: url.into() }.into())
					.widget_instance()
			})
			.collect::<Vec<_>>();

		// Cloning here and below seems to be necessary to appease the borrow checker, as far as I can tell.
		let localized_commit_year = self.localized_commit_year.clone();
		widgets.push(
			TextButton::new("Licenses")
				.icon("License")
				.flush(true)
				.on_update(move |_| {
					DialogMessage::RequestLicensesDialogWithLocalizedCommitDate {
						localized_commit_year: localized_commit_year.clone(),
					}
					.into()
				})
				.widget_instance(),
		);

		Layout(vec![LayoutGroup::column(widgets)])
	}
}

impl LayoutHolder for AboutGraphiteDialog {
	fn layout(&self) -> Layout {
		Layout(vec![
			LayoutGroup::row(vec![TextLabel::new(photocoop_identity::ABOUT_HEADING).bold(true).widget_instance()]),
			LayoutGroup::row(vec![
				TextLabel::new(photocoop_identity::about_body(&self.localized_commit_date, &self.localized_commit_year))
					.multiline(true)
					.widget_instance(),
			]),
		])
	}
}
