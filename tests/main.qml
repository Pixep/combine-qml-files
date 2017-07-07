Item {
	//---------------
	// @Button
	Rectangle {
	    color: baseColor
	    width: 100
	    height: 30
	
	    Text {
	        anchors.centerIn: parent
	    }
	    //---- Redefinitions ----
		text: "toto"
	}

	Toto {
		color: "blue"

		//---------------
		// @Button
		Rectangle {
		    color: baseColor
		    width: 100
		    height: 30
		
		    Text {
		        anchors.centerIn: parent
		    }
		    //---- Redefinitions ----
			text: "toto"
			Text {

			}
		}
	}
}
