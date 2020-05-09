import React from 'react';
import {View, Text, FlatList, TouchableOpacity} from 'react-native';

class RoomsScreen extends React.Component {
  onRoomPress = () => {
    this.props.navigation.navigate('Chat');
  };

  renderItem = (item, index) => {
    return (
      <TouchableOpacity
        key={index}
        style={{padding: 20}}
        onPress={this.onRoomPress}>
        <Text>sdffgh</Text>
      </TouchableOpacity>
    );
  };
  render() {
    return (
      <FlatList
        data={[0, 1, 2, 34]}
        renderItem={this.renderItem}
        keyExtractor={(item, index) => '' + index}
      />
    );
  }
}

export default RoomsScreen;
