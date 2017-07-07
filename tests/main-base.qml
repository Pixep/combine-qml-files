Item {
	@Button {
		text: "final text"
	}

	Rectangle {
		color: "blue"

		@Button {
			text: "other text"
			Rectangle {
				anchors.fill: parent
				color: Qt.rgba(0, 0, 0, 0.3)
			}
		}
	}
}
