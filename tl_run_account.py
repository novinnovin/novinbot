import os, re, sys, time, datetime, telethon, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg
    elif index == 2:
        order_id = int(arg)

directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.admin}")
row_admin = cs.fetchone()
cs.execute(f"SELECT * FROM {utl.orders} WHERE id={order_id}")
row_orders = cs.fetchone()
cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()

utl.get_params_pids_by_full_script_name(script_names=[f"{directory}/{filename}"], param1=row_mbots["uniq_id"], is_kill_proccess=True)


def check_report(client):
    try:
        for r in client(telethon.functions.messages.StartBotRequest(bot="@spambot", peer="@spambot", start_param="start")).updates:
            for r1 in client(telethon.functions.messages.GetMessagesRequest(id=[r.id + 1])).messages:
                if "I’m afraid some Telegram users found your messages annoying and forwarded them to our team of moderators for inspection." in r1.message:
                    if "Unfortunately, your account is now limited" in r1.message:
                        return int(time.time()) + 604800
                    else:
                        regex = re.findall('automatically released on [\d\w ,:]*UTC', r1.message)[0]
                        regex = regex.replace("automatically released on ","")
                        regex = regex.replace(" UTC","")
                        restrict = datetime.datetime.strptime(regex, "%d %b %Y, %H:%M").timestamp()
                        return restrict
                elif "While the account is limited, you will not be able to send messages to people who do not have your number in their phone contacts" in r1.message:
                    return int(time.time()) + 604800
            break
    except:
        pass
    return False


def operation(cs, row_orders, row_mbots, result_reports):
    try:
        cs.execute(f"INSERT INTO {utl.usedaccs} (order_id,bot_id,created_at) VALUES ({row_orders['id']},{row_mbots['id']},{int(time.time())})")
        cs.execute(f"UPDATE {utl.mbots} SET last_order_at={int(time.time())} WHERE id={row_mbots['id']}")
        cs.execute(f"UPDATE {utl.orders} SET count_acc=count_acc+1 WHERE id={row_orders['id']}")
        count_join = 0

        client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
        client.connect()
        if not client.is_user_authorized():
            cs.execute(f"UPDATE {utl.mbots} SET status=0 WHERE id={row_mbots['id']}")
            cs.execute(f"UPDATE {utl.orders} SET count_accout=count_accout+1 WHERE id={row_orders['id']}")
            return print(f"{row_mbots['id']}: Log Out")
        
        restrict = check_report(client)
        if restrict:
            cs.execute(f"UPDATE {utl.mbots} SET status=2,end_restrict={restrict} WHERE id={row_mbots['id']}")
            cs.execute(f"UPDATE {utl.orders} SET count_report=count_report+1 WHERE id={row_orders['id']}")
            return print(f"{row_mbots['id']}: Limited")
        
        limit_per_h = int(time.time()) + row_admin['limit_per_h']
        cs.execute(f"UPDATE {utl.mbots} SET status=2,end_restrict={limit_per_h} WHERE id={row_mbots['id']}")
        try:
            link = row_orders['destination']
            try:
                client(telethon.functions.channels.GetParticipantRequest(channel=link,participant="me"))
            except:
                try:
                    if "/joinchat/" in link:
                        client(telethon.functions.messages.ImportChatInviteRequest(link.split("/joinchat/")[1]))
                    else:
                        client(telethon.functions.channels.JoinChannelRequest(channel=link))
                except telethon.errors.UserAlreadyParticipantError as e:
                    pass
            chat_destination = int(row_orders['destination_id'][4:])
        except telethon.errors.FloodWaitError as e:
            print(f"{row_mbots['phone']}: {e}")
            end_restrict = int(time.time()) + int(e.seconds)
            if end_restrict > limit_per_h:
                cs.execute(f"UPDATE {utl.mbots} SET status=2,end_restrict={end_restrict} WHERE id={row_mbots['id']}")
            return cs.execute(f"UPDATE {utl.orders} SET count_accrestrict=count_accrestrict+1 WHERE id={row_orders['id']}")
        except telethon.errors.ChatWriteForbiddenError as e:
            print(f"{row_mbots['phone']}: {e}")
            return cs.execute(f"UPDATE {utl.orders} SET count_accpermission=count_accpermission+1 WHERE id={row_orders['id']}")
        except telethon.errors.UserBannedInChannelError as e:
            print(f"{row_mbots['phone']}: {e}")
            return cs.execute(f"UPDATE {utl.orders} SET count_accban=count_accban+1 WHERE id={row_orders['id']}")
        except Exception as e:
            print(f"{row_mbots['phone']}: {e}")
            return cs.execute(f"UPDATE {utl.orders} SET count_accotheerror=count_accotheerror+1 WHERE id={row_orders['id']}")
        for row_reports in result_reports:
            cs.execute(f"UPDATE {utl.reports} SET bot_id={row_mbots['id']},status=2 WHERE id={row_reports['id']}")
            cs.execute(f"UPDATE {utl.orders} SET last_member_check=last_member_check+1 WHERE id={row_orders['id']}")
            try:
                client(telethon.functions.channels.GetParticipantRequest(channel=chat_destination, participant=row_reports['username']))
                cs.execute(f"UPDATE {utl.orders} SET count_usrrepeat=count_usrrepeat+1 WHERE id={row_orders['id']}")
                print(f"{row_mbots['phone']} ({row_reports['username']}): Already")
            except telethon.errors.UserNotParticipantError as e:
                try:
                    result = client(telethon.functions.channels.InviteToChannelRequest(channel=chat_destination, users=[row_reports['username']]))
                    for user in result.updates.users:
                        # if isinstance(row, telethon.types.UpdateReadChannelInbox):
                        if isinstance(user, telethon.types.User) and user.id != row_mbots['user_id']:
                            cs.execute(f"UPDATE {utl.reports} SET bot_id={row_mbots['id']},status=1 WHERE id={row_reports['id']}")
                            cs.execute(f"UPDATE {utl.orders} SET count_moved=count_moved+1 WHERE id={row_orders['id']}")
                            print(f"{row_mbots['phone']} ({row_reports['username']}): Joined")
                            count_join += 1
                            if (row_orders['count_moved'] + count_join) >= row_orders['count']:
                                cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']} AND count_moved>0 AND count_moved>=count")
                                if cs.fetchone() is not None:
                                    return
                        # elif isinstance(row, telethon.types.UpdateGroupInvitePrivacyForbidden):
                        #     cs.execute(f"UPDATE {utl.orders} SET count_usrprivacy=count_usrprivacy+1 WHERE id={row_orders['id']}")
                        #     break
                        # else:
                        #     print(result.updates)
                        #     print(result.users)
                        #     print()
                except telethon.errors.FloodWaitError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): FloodWaitError when Invite")
                    end_restrict = int(time.time()) + int(e.seconds)
                    if end_restrict > limit_per_h:
                        cs.execute(f"UPDATE {utl.mbots} SET status=2,end_restrict={end_restrict} WHERE id={row_mbots['id']}")
                    cs.execute(f"UPDATE {utl.orders} SET count_accrestrict=count_accrestrict+1 WHERE id={row_orders['id']}")
                    return
                except telethon.errors.UserPrivacyRestrictedError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): UserPrivacyRestrictedError")
                    cs.execute(f"UPDATE {utl.orders} SET count_usrprivacy=count_usrprivacy+1 WHERE id={row_orders['id']}")
                except telethon.errors.UserNotMutualContactError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): UserNotMutualContactError")
                    cs.execute(f"UPDATE {utl.orders} SET count_usrprivacy=count_usrprivacy+1 WHERE id={row_orders['id']}")
                except telethon.errors.UserChannelsTooMuchError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): UserChannelsTooMuchError")
                    cs.execute(f"UPDATE {utl.orders} SET count_usrtoomuch=count_usrtoomuch+1 WHERE id={row_orders['id']}")
                except telethon.errors.UserKickedError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): UserKickedError")
                    cs.execute(f"UPDATE {utl.orders} SET count_usrban=count_usrban+1 WHERE id={row_orders['id']}")
                except telethon.errors.ChatWriteForbiddenError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): ChatWriteForbiddenError")
                    cs.execute(f"UPDATE {utl.orders} SET count_accpermission=count_accpermission+1 WHERE id={row_orders['id']}")
                    return
                except telethon.errors.UserBannedInChannelError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): UserBannedInChannelError")
                    cs.execute(f"UPDATE {utl.orders} SET count_accban=count_accban+1 WHERE id={row_orders['id']}")
                    return
                except telethon.errors.ChannelPrivateError as e:
                    print(f"{row_mbots['phone']} ({row_reports['username']}): ChannelPrivateError")
                    cs.execute(f"UPDATE {utl.orders} SET count_accban=count_accban+1 WHERE id={row_orders['id']}")
                    return
                except Exception as e:
                    error = str(e)
                    print(f"{row_mbots['phone']} ({row_reports['username']}): Error when Invite: {error}")
                    if error == 'Too many requests (caused by InviteToChannelRequest)':
                        cs.execute(f"UPDATE {utl.orders} SET count_usrspam=count_usrspam+1 WHERE id={row_orders['id']}")
                    else:
                        cs.execute(f"UPDATE {utl.orders} SET count_usrotheerror=count_usrotheerror+1 WHERE id={row_orders['id']}")
            except telethon.errors.FloodWaitError as e:
                print(f"{row_mbots['phone']} ({row_reports['username']}): FloodWaitError when Invite")
                end_restrict = int(time.time()) + int(e.seconds)
                if end_restrict > limit_per_h:
                    cs.execute(f"UPDATE {utl.mbots} SET status=2,end_restrict={end_restrict} WHERE id={row_mbots['id']}")
                cs.execute(f"UPDATE {utl.orders} SET count_accrestrict=count_accrestrict+1 WHERE id={row_orders['id']}")
                return
            except Exception as e:
                cs.execute(f"UPDATE {utl.orders} SET count_usrotheerror=count_usrotheerror+1 WHERE id={row_orders['id']}")
                print(f"{row_mbots['phone']} ({row_reports['username']}): GetParticipantRequest: {e}")
    except Exception as e:
        print(f"{row_mbots['phone']}: {e}")
    finally:
        try:
            client.disconnect()
            print(f"{row_mbots['phone']} RESULT: {count_join}")
        except:
            pass


if row_orders is not None and row_mbots is not None:
    cs.execute(f"SELECT * FROM {utl.reports} WHERE order_id={row_orders['id']} AND status=0 LIMIT {row_orders['add_per_h']}")
    result_reports = cs.fetchall()
    if result_reports:
        operation(cs, row_orders, row_mbots, result_reports)
    else:
        cs.execute(f"UPDATE {utl.orders} SET status=2,updated_at={int(time.time())} WHERE id={row_orders['id']}")

