Item {
	//---------------
	// @Button
	Text {
	    color: "gray"
	    width: 100
	    height: 30
	
	    MouseArea {}
	    //---- Redefinitions ----
		text: "final text"
	}

	Rectangle {
		color: "blue"

		//---------------
		// @Button
		Text {
		    width: 100
		    height: 30
		
		    MouseArea {}
		    //---- Redefinitions ----
			text: "other text"
			Rectangle {
				anchors.fill: parent
				color: Qt.rgba(0, 0, 0, 0.3)
			}
		}
	}
}
