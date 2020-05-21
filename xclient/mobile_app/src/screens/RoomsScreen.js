import React from 'react';
import {View, Text, FlatList, TouchableOpacity, StyleSheet} from 'react-native';

class RoomsScreen extends React.Component {
  onRoomPress = () => {
    this.props.navigation.navigate('Chat');
  };

  renderItem = (item, index) => {
    return (
      <TouchableOpacity
        key={index}
        style={styles.itemContainer}
        onPress={this.onRoomPress}>
        <Text>sdffgh</Text>
      </TouchableOpacity>
    );
  };
  render() {
    return (
      <FlatList
        style={styles.itemContainer}
        contentContainerStyle={styles.listContentContainer}
        data={[0, 1, 2, 34]}
        ItemSeparatorComponent={() => (
          <View style={{borderBottomWidth: StyleSheet.hairlineWidth}} />
        )}
        renderItem={this.renderItem}
        keyExtractor={(item, index) => '' + index}
      />
    );
  }
}

const styles = StyleSheet.create({
  listContainer: {
    backgroundColor: 'white',
  },
  listContentContainer: {
    paddingBottom: 20,
  },
  itemContainer: {
    marginHorizontal: 5,
    padding: 20,
    borderRadius: 10,
  },
});

export default RoomsScreen;
