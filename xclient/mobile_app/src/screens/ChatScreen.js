import React from 'react';
import {View, Text, Button, StyleSheet} from 'react-native';
import {GiftedChat} from 'react-native-gifted-chat';

class ChatScreen extends React.Component {
  constructor(props) {
    super(props);

    this.props.navigation.setOptions({
      headerRight: () => (
        <Button onPress={this.onRoomPress} title="Info" color="#fff" />
      ),
    });
  }
  state = {
    messages: [],
  };

  componentDidMount() {
    this.setState({
      messages: [
        {
          _id: 1,
          text: 'Hello developer',
          createdAt: new Date(),
          user: {
            _id: 2,
            name: 'React Native',
            avatar:
              'https://static.fajnyzwierzak.pl/media/uploads/media_image/original/wpis/355/jamnik-merle.jpg',
          },
        },
        {
          _id: 2,
          text: 'Hello sd',
          createdAt: new Date(),
          user: {
            _id: 2,
            name: 'React Native',
            avatar:
              'https://static.fajnyzwierzak.pl/media/uploads/media_image/original/wpis/355/jamnik-merle.jpg',
          },
        },

        {
          _id: 3,
          text: 'Hello sdf',
          createdAt: new Date(),
          user: {
            _id: 3,
            name: 'React Native',
            avatar:
              'https://thumbs.img-sprzedajemy.pl/1000x901c/4a/ae/50/jamnik-kroliczy-krotkowlosy-szczeniak-legnica-504917692.jpg',
          },
        },
        {
          _id: 4,
          text: 'Hello sd',
          createdAt: new Date(),
          user: {
            _id: 2,
            name: 'React Native',
            avatar:
              'https://static.fajnyzwierzak.pl/media/uploads/media_image/original/wpis/355/jamnik-merle.jpg',
          },
        },
      ],
    });
  }

  onSend(messages = []) {
    this.setState(previousState => ({
      messages: GiftedChat.append(previousState.messages, messages),
    }));
  }

  render() {
    return (
      <View style={styles.container}>
        <GiftedChat
          isTyping
          messages={this.state.messages}
          onSend={messages => this.onSend(messages)}
          user={{
            _id: 1,
            name: 'seba',
          }}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    flex: 1,
    backgroundColor: 'white',
  },
});
export default ChatScreen;
